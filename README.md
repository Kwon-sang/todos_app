# [FastAPI] Todos Application API Server Project

---

## Contents
- Introductions
- 1.API Web Page (OpenAPI)
- 2.Project Settings
- 3.Project Structure
- 4.Endpoints
- 5.Main Logic

</br>

# Introductions
**FastAPI** 를 사용한 일정관리 어플리케이션 API 서버 프로젝트 입니다.

</br>

 #### ✔️프로젝트 구성에 대하여
- 프로젝트 패키지의 구성은 RESTful API의 관점에서 고민하여, 각 **엔드포인트의 루트 리소스 관점**으로 구성하였습니다.
- API 리소스 루트는 기능에 따라, `/admin`, `/auth`, `/todos`, `/users` 로 구분됩니다.
- 따라서, 프로젝트 패키지 또한 이러한 형태로 구성하여 관리가 용이하도록 구성하였습니다.
- 유저에 관한 api 모델, 로직의 변경 혹은 참조가 필요할 경우, `user` 패키지에 관련된 부분들이 있음을 알 수 있습니다.

</br>

 #### ✔️ Model 과 Schema의 분리
>`SQL Model`과 `pydantic Model` 를 구분 하였습니다. `SQL Model`은 ODM(Object Data Mapping) 객체로, `pydantic Model`은 DTO(Data Transfer Object) 및 validator로, 사용 목적을 명확히 분리하고자 하였습니다.</br>
> ODM 객체인 **SQL Model은 DB layer에 대한 제약조건 책임**을 가집니다. 관계를 정의하며, 유니크 옵션 등 DB 레벨의 제약을 정의합니다. </br>
>**pydantic Model은 Http reqeust/response data validation layer에 대한 책임**을 가집니다. 가장 먼저 입력값의 스키마 제약을 검증합니다. </br>

</br>

 #### ✔️ DB Connection과 JWT Authorization
>토이 프로젝트 목적으로 사용하기 간편한 SQLite Databse를 사용하여 DB Connection을 구성하였으며, </br>
>권한/인증을 위해 **JWT Bearer Authentication**을 사용하였습니다.</br>

</br>

 #### ✔️ Secrey key 및 동적인 시스템 환경 세팅을 위한 로컬 머신 환경변수 파일 세팅
>Database URL 및 JWT Secret key 와 같은 보안이 필요한 변수들은 머신 `.env` 파일로 관리할 수 있으며,</br>
>`.env` 파일에서 `ENVSTATUS` 변수를 통해 **동적으로 개발환경/테스트환경/운영환경의 전환**이 가능하도록 설정하였습니다. </br>

</br>

 #### ✔️ 재사용이 빈번한 DB CRUD를 `database.py` 모듈에 위임하여, 유연하고 재사용가능하도록 구성
> CRUD 기능을 유연하게 확장하기 위해서는 `Session.query(Model).filter(option1, option2, ...)` 와 같이,
> 동적으로 필터링 조건이 확장될 수 있어야 합니다.<br>
> 이에 대한 로직을 고민하였으며, `eval`을 사용하여, 함수 호출 파라미터를 `filter` 옵션으로 동적 할당 및 사용가능한 로직을 구현하였습니다.

 #### ✔️ CRUD DB I/O 최적화
> 대부분의 참고 자료와 도서에서는 CRUD 기능을 수행함에 있어서, '해당 데이터의 존재여부' / '실행' 과 같이, 
> 하나의 기능을 위해 두번의 DB I/O가 발생하는 것을 확인하였습니다. </br>
> 이에 대해 한번의 SQL을 통해 수행가능하도록 구문을 구성하였으며, **불필요한 DB I/O를 줄일 수 있도록 구성**하였습니다. 

#### ✔️ `pytest`를 통한 Endpoint testing
> 기능을 변경하고, 리팩토링 함에 있어서 일일히 웹페이지를 통해 기능을 테스트 하는것에 한계를 느끼게 되었습니다.
> 따라서, `pytest`를 통해 **테스트 로직을 구성**하였으며, 빠르게 기능 변경의 동작을 확인할 수 있도록 하였습니다.

</br>

## 1. API Web Page (OpenAPI)
<img width="1200" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3337fa03-800f-4251-80e6-5d33d006f7a3">
<img width="1184" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3bee2438-22f8-4ef0-ae5f-736a88c44b52">


</br>
</br>

## 2. Project Settings
- Python version management system : `pyenv`
- Package management system : `poetry`
- Database : `SQLite3`


</br>
</br>

## 3. Project Structure
- Project root
  - src
    - auth/
    - admin/
    - todos/
    - users/
    - database.py
    - settings.py (environment variable setting)
    - main.py
  - test/
  - poetry.lock
  - pyproject.toml
  - .env

</br>
</br>

## 4. Endpoints

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


</br>
</br>

## 5. Main logic

>- DB CRUD session의 재사용성을 고민하였으며, 이를 달성하기 위한 로직을 구성하였습니다. </br>
>- CRUD 기능은 endpoint 마다 DB 쿼리를 위해 반복적으로 사용되며, DB에 관한 로직을 DB 모듈에서 관리할 경우 보다 가벼운 router 를 만들어 낼 수 있습니다. </br>
>- 여기서 관건은, 각 endpoint 마다 서로 다른 조회 조건을 가질 수 있으며 이러한 상이한 조건에 대해서도 유연해야 합니다. 해당 조건의 개수에 따라 동적으로 `Session.query.filter` 옵션에 적용되어야 합니다.</br>
>- 이 문제를 해결하기 위해 `eval` 기능을 이용한 `filtering_condition_creator(model, **kwargs)` 함수를 구현하였습니다. </br>
>- 해당 함수는 필터링 조건을 키워드 인자를 통해 동적으로 filter 조건을 만들어내며, 상이한 조건 및 조건의 개수에도 유연합니다.

Example)
```
# DB 조회 사용자 정의 함수
retrieve_all(User, id=some_id, owner=some_user_id)

# 아래와 동일하게 적용됩니다. 조건의 개수와 상관없이 동적으로 필터링 조건을 만들어 냅니다.
Session.query(User).filter(id == some_id, owner == some_user_id).all() 
```

이 기능은 다음과 같은 함수에 의해 구현됩니다. 
이 함수는 조건에 대한 인자를 키워드 인자로 받아, DB Session `filter(options)` 에서 사용가능한 형태로 변형하여 주입합니다.
필터링 조건은 사용자에 따라 동적으로 변경되기에, `list`에 변형된 조건 인자를 `eval`로 담아 파라미터로 실행가능한 상태를 유지합니다. 
```
def filtering_condition_creator(model, **kwargs) -> list[Any]:
    """
    키워드 인자를 filter 인자로 사용할 수 있게 변환하는 함수 입니다.
    eval을 통해 평가된 조건 인자를 리스트에 저장하여 반환합니다.
    ex)
    filtering = filtering_condition_creator(User, id=1, username="kim")
    filtering -> [eval(User.id == 1), eval(User.username == "kim")]
    Session.query(User).filter(*filtering) -> Session.query(User).filter(User.id == 1, User.username == "kim")
    """
    conditions = []
    for key, value in kwargs.items():
        if key not in model.model_fields:
            raise KeyError(f"Field name {key!r} is not found in {model.__name__}")
        conditions.append(eval(f"model.{key} == {value!r}"))
    return conditions

# 함수 호출
conditions = filtering_condition_creator(model, **kwargs)
# 필터링 조건 실행
result = db.query(model).filter(*conditions).first()
```




