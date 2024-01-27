# [FastAPI] Todos Application API Server Project

---

## Contents
- Introductions
- 1.API Web Page (OpenAPI)
- 2.Project Settings
- 3.Project Structure
- 4.Main Logic

</br>

## Introductions
Microservice에 특화 된 **FastAPI** 를 사용한 일정관리 어플리케이션 API 서버 프로젝트 입니다.

---

 #### ✔️프로젝트 구성에 대하여
>프로젝트 패키지의 구성은 RESTful API의 관점에서 고민하여, 각 **엔드포인트의 루트 리소스 관점**으로 구성하였습니다.</br>
>API 리소스 루트는 기능에 따라, `/admin`, `/auth`, `/todos`, `/users` 로 구분됩니다. </br>
>따라서, 프로젝트 패키지 또한 이러한 형태로 구성하여 관리가 용이하도록 구성하였습니다.

 #### ✔️ Model 과 Schema의 분리
>`SQL Model`과 `pydantic Model` 를 구분 하였습니다. </br>
>각각 서로 다른 목적과 책임을 갖기에, </br>
> ODM 객체인 **SQL Model은 DB layer에 대한 제약조건 책임**을, </br>
>**pydantic Model은 Http reqeust/response data validation layer에 대한 책임**으로 분할하였습니다. </br>
>models 모듈은 `SQLModel` 로, schemas 모듈은 `pydantic.BaseModel` 로 관리합니다.

 #### ✔️ DB Connection과 JWT Authorization
>토이 프로젝트 목적으로 사용하기 간편한 SQLite Databse를 사용하여 DB Connection을 구성하였으며, </br>
>권한/인증을 위해 JWT Bearer Authentication을 사용하였습니다.</br>

 #### ✔️ Secrey key 및 동적인 시스템 환경 세팅을 위한 로컬 머신 환경변수 파일 세팅
>Database URL 및 JWT Secret key 와 같은 보안이 필요한 변수들은 머신 `.env` 파일로 관리할 수 있으며,</br>
>`.env` 파일에서 `ENVSTATUS` 변수를 통해 동적으로 개발환경/테스트환경/운영환경의 전환이 가능하도록 설정하였습니다. </br>

 #### ✔️ 재사용이 빈번한 DB CRUD를 `database.py` 모듈에 위임하여, 유연하고 재사용가능하도록 구성
> CRUD 기능을 유연하게 확장하기 위해서는 `Session.query(Model).filter(option1, option2, ...)` 와 같이,
> 동적으로 필터링 조건이 확장될 수 있어야 합니다.<br>
> 이에 대한 로직을 고민하였으며, `eval`을 사용하여, 함수 호출 파라미터를 `filter` 옵션으로 동적 할당 및 사용가능한 로직을 구현하였습니다.

 #### ✔️ CRUD DB I/O 최적화
> 대부분의 참고 자료와 도서에서는 CRUD 기능을 수행함에 있어서, '해당 데이터의 존재여부' / '실행' 과 같이, 
> 하나의 기능을 위해 두번의 DB I/O가 발생하는 것을 확인하였습니다. </br>
> 이에 대해 한번의 SQL을 통해 수행가능하도록 구문을 구성하였으며, 불필요한 DB I/O를 줄일 수 있도록 구성하였습니다. 

#### ✔️ `pytest`를 통한 Endpoint testing
> 기능을 변경하고, 리팩토링 함에 있어서 일일히 웹페이지를 통해 기능을 테스트 하는것에 한계를 느끼게 되었습니다.
> 따라서, `pytest`를 통해 테스트 로직을 구성하였으며, 빠르게 기능 변경의 동작을 확인할 수 있도록 하였습니다.

</br>

## 1. API Web Page (OpenAPI)
<img width="1200" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3337fa03-800f-4251-80e6-5d33d006f7a3">
<img width="1184" alt="image" src="https://github.com/Kwon-sang/todos_app/assets/115248448/3bee2438-22f8-4ef0-ae5f-736a88c44b52">


</br>

## 2. Project Settings
- Python version management system : `pyenv`
- Package management system : `poetry`
- Database : `SQLite3`

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


