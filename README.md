# [FastAPI] Todos Application API Server Project

</br>
</br>

## Contents
- Introductions
- API Web Page Image (OpenAPI)
- Project Settings
- Project Structure
- Endpoints

</br>
</br>

# Introductions

**FastAPI** 를 사용한 일정관리 어플리케이션 API 서버 프로젝트 입니다.

</br>

 #### ✔️프로젝트 구성에 대하여
- 프로젝트 패키지의 구성은 RESTful API의 관점에서 고민하여, 각 **엔드포인트의 루트 리소스 관점**으로 구성하였습니다.
- API 리소스 루트는 기능에 따라, `/admin`, `/auth`, `/todos`, `/users` 로 구분됩니다.
- 따라서, **Project Structure** 또한 이러한 `/admin`, `/auth`, `/todos`, `/users` 구성하여 관리가 용이하도록 구성하였습니다.
- 유저에 관한 api 모델, 로직의 변경 혹은 참조가 필요할 경우, `user` 패키지에 관련된 부분들이 있을 것임을 쉽게 유추할 수 있습니다.

</br>

 #### ✔️ Model 과 Schema의 분리
- Data Model Schema를 정의함에 있어, `SQL Model`과 `pydantic Model`을 구분 하였습니다.
- `SQL Model`은 ODM(Object Data Mapping) 객체로, `pydantic Model`은 DTO(Data Transfer Object) 및 validator로, 사용 목적을 명확히 분리하고자 하였습니다.</br>
-  ODM 객체인 **SQL Model은 DB layer에 대한 제약조건 책임**을 가집니다. 관계를 정의하며, 유니크 옵션 등 DB 레벨의 제약을 정의합니다. </br>
- **pydantic Model은 Http reqeust/response data validation layer에 대한 책임**을 가집니다. Request Body의 타입 및 필수필드를 검증합니다. </br>

</br>

 #### ✔️ DB 과 JWT Authorization
- 토이 프로젝트 목적으로, 사용하기 간편한 **SQLite Databse**를 사용하였습니다. </br>
- **권한/인증**을 위해 **JWT Bearer Authentication**을 사용하였습니다.</br>
- 현재 프로젝트에서, DB I/O는 **Synchronous Session**을 사용하였으나, **Asynchonous Session**으로 변경 가능하며, 이를 통해 DB I/O session의 처리 성능을 개선할 수 있습니다. 

</br>

 #### ✔️ 개발/운영/테스트 환경을 동적으로 설정 및 Secret key 보안
- 개발환경/운영환경/테스트환경을 동적으로 유연하게 변경될 수 있어야 하며, 또한 SECREY KEY와 같은 보안 환경변수를 외부에 노출되지 않도록 안전하게 보관할 수 있어야 합니다.
- `.env` 환경변수 파일을 사용하여 **보안이 필요한 변수를 환경 변수로** 설정하였으며, **개발/운영/테스트 환경에 따라 유연하게 사용가능**하도록 구성하였습니다.
- `.env` 파일에서 `ENV_STATUS` 변수를 통해 **동적으로 개발환경/테스트환경/운영환경의 전환**이 가능합니다.
- `settings.py`은 이러한 로직을 담당합니다.

[`src/settings.py`의 링크 입니다.](https://github.com/Kwon-sang/todos_app/blob/master/src/settings.py)
[`.env` 환경변수 파일의 링크입니다.](https://github.com/Kwon-sang/todos_app/blob/master/.env) 


</br>

 #### ✔️ 재사용이 빈번한 DB CRUD를 `database.py` 모듈에 위임하여, 유연하고 재사용가능하도록 구성
- 대부분의 Router마다, CRUD 기능을 구현하며, 여기서 많은 **중복이 발생**합니다.
- 반복적으로 사용되는 CRUD 로직을 `database.py`에 위임하여, **중복을 줄이고**, **재사용성을 증대**시키고자 하였습니다.
- CRUD 기능을 유연하게 확장하기 위해서는 `Session.query(Model).filter(**option1, option2, ...**)` 와 같이, 동적으로 필터링 조건이 확장될 수 있어야 합니다.
- 이에 대한 로직을 고민하였으며, `eval`을 사용하여, 함수 호출 파라미터를 `filter` 옵션으로 동적 할당 및 사용가능한 로직을 구현하였습니다.

> 예를 들어, A, B, C 등의 함수는 Z라는 함수를 공통적으로 이용하되, Z 함수의 인자는 가변적인 boolean expression 인자를 가질 경우 (ex. id == 1, name == '홍길동'), </br>
> Z 함수를 사용하기 위해, Z 함수의 인자의 개수는 동적으로 할당되어야 하며, 동시에 boolean expression 으로 표현되어야 합니다.</br>
> 이 동작을 구현하기 위해 `eval` 기능을 이용하여, String 형태로 조작하며 excutable 하도록 하였습니다.

[`src/database.py`, `filtering_condition_creator` 함수](https://github.com/Kwon-sang/todos_app/blob/master/src/database.py)

</br>

 #### ✔️ CRUD DB I/O 최적화
- 대부분의 참고 자료와 도서에서는 CRUD 기능을 수행함에 있어서, **해당 데이터가 존재하는지 조회 쿼리 수행**, **메인 실행 쿼리 수행** 과 같이, 하나의 기능을 위해 **두번의 DB I/O**가 발생하는 것을 확인하였습니다.
- 이는 불필요한 로직이라 판단하였으며, 한번의 쿼리 실행으로 동일한 동작을 제어할 수 있을 것으로 생각하였으며 이를 적용하였습니다.
- 실행되는 불필요한 DB I/O 를 줄일 수 있었으며 이를 통해 성능이 근소하게 향상되었습니다.

</br>

#### ✔️ `pytest`를 통한 Endpoint testing
> 기능을 변경하고, 리팩토링 함에 있어서 일일히 웹페이지를 통해 기능을 테스트 하는것에 한계를 느끼게 되었습니다.
> 따라서, `pytest`를 통해 **테스트 로직을 구성**하였으며, 빠르게 기능 변경의 동작을 확인할 수 있도록 하였습니다.

</br>
</br>

# API Web Page Image (OpenAPI)
<img width="1200" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3337fa03-800f-4251-80e6-5d33d006f7a3">
<img width="1184" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3bee2438-22f8-4ef0-ae5f-736a88c44b52">


</br>
</br>

# Project Settings

- Python version management system : `pyenv`
- Package management system : `poetry`
- Languege : `python 3.11`
- Web-framework : `FastAPI`
- Database : `SQLite3`
- Testing module : `pytest`
- ORM : `SQLalchemy 2.0`


</br>
</br>

# Project Structures

- Project root
  - src
    - auth
      - `routes.py`
      - `schemas.py`
      - `service.py`
    - admin
      - `routes.py`
    - todos
      - `routes.py`
      - `models.py`
      - `schemas.py` 
    - users
      - `routes.py`
      - `models.py`
      - `schemas.py` 
    - `database.py`
    - `settings.py` (environment variable setting)
    - `main.py`
  - test/
  - poetry.lock
  - pyproject.toml
  - .env

</br>
</br>

# Endpoints

**/auth**
> JWT Access Token 발행
- `PUT` /auth

**/users**
> 유저 기능. 해당 엔드포인트는 현재 접속한 유저에 유효 합니다.
- `POST` /users : 유저 생성 (HTTP status code 201 create)
- `GET` /users/{user_id} : 유저 정보 조회 (HTTP status code 200 ok). 생성된 리소스를 반환.
- `PUT` /users/{user_id} : 유저 정보 수정 (HTTP status code 204 no content)
- `PATCH` /users/{user_id}/password : 유저 패스워드 변경 (HTTP status code 204 no content)

**/todos**
> Todo 일정관리 기능. 해당 엔드포인트는 현재 접속한 유저에 유효 합니다.
- `GET` /todos : 모든 Todo 조회(HTTP status code 200 ok)
- `POST` /todos : 새 Todo 생성(HTTP status code 201 create)
- `GET` /todos/{todo_id} : 하나의 Todo를 id 조회(HTTP status code 200 ok)
- `PUT` /todos/{todo_id} : Todo 리소스 수정(HTTP status code 204 no content)
- `DELETE` /todos/{todo_id} : Todo 리소스 제거(HTTP status code 204 no content)

**/admin**
> Administor 기능. 해당 엔드포인트는 "admin" role을 가진 유저에 한함. (일반 유저 role : "user")
- `GET` /admin/users : 시스템 내 모든 유저 정보 조회 (HTTP status code 200 ok)
- `GET` /admin/todos : 시스템 내 모든 Todo 정보 조회 (HTTP status code 200 ok)
- `PATCH` /admin/{user_id}/role : 유저 권한 변경 (HTTP status code 204 no content)
- `PATCH` /admin/{user_id}/active : 유저 활성화 상태 변경 (HTTP status code 204 no content)





