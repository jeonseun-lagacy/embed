//아이디 입력 인풋
const id = document.getElementById('id');

//비밀번호, 비밀번호 재입력 인풋
const password = document.getElementById('password');
const passwordRepeat = document.getElementById('passwordRepeat');

//ID 중복확인 여부
let isIdChecked = false;
//비밀번호, 비밀번호 확인 동일 여부
let isPasswordChecked = false;

//회원가입 가능 여부 검사 후 가입 버튼 활성화
function validate() {
    const signupBtn = document.getElementById('signUpBtn');
    if (isIdChecked && isPasswordChecked) {
        signupBtn.disabled = false;
    } else {
        signupBtn.disabled = true;
    }
}

//id 중복확인 함수
function isIdDoubled() {
    if (id.value == "") {
        alert('아이디를 입력하세요');
    } else if (id.value.length > 16) {
        alert('아이디 길이 초과');
    } else {
        const jsonData = {
            id: id.value
        };
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const result = JSON.parse(xhr.responseText);
                console.log(xhr.responseText);
                if (result.existence === "false") {
                    console.log('ID 사용가능');
                    alert('사용가능');
                    isIdChecked = true;
                } else {
                    console.log('ID 사용불가');
                    alert('사용불가');
                    isIdChecked = false;
                }
                validate();
            }
        }
        xhr.open('post', '/id', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(jsonData));
    }
}

//비밀번호 및 아이디 길이 제한 및 비밀번호 입력, 재입력 확인
function init() {
    id.addEventListener('input', function () {
        isIdChecked = false;
        checkInputLength(id);
    });

    password.addEventListener('input', function () {
        isPasswordChecked = false;
        checkInputLength(password);
    });

    passwordRepeat.addEventListener('input', function () {
        isPasswordChecked = false;
        checkInputLength(passwordRepeat);
    });

    passwordRepeat.addEventListener('input', isPasswordEqual);

    function isPasswordEqual() {
        if (password.value == passwordRepeat.value) {
            passwordRepeat.classList.remove('bg-danger');
            passwordRepeat.classList.add('bg-success');
            isPasswordChecked = true;
        } else {
            passwordRepeat.classList.remove('bg-success');
            passwordRepeat.classList.add('bg-danger');
        }
        validate();
    }

    function checkInputLength(container) {
        if (container.value.length > 16) {
            container.classList.remove('bg-success');
            container.classList.add('bg-danger');
        } else {
            container.classList.remove('bg-danger');
            container.classList.add('bg-success');
        }
        validate();
    }

    selectSignUpType();
}


//점장 가입, 직원 가입 구분 버튼 이벤트
function selectSignUpType() {
    //가입 유형 선택 버튼 컨테이너
    const signUpSelectorContainer = document.getElementById('signUpSelector');

    //가입 유형 선택 버튼
    const managerSignUpBtn = document.getElementById('signUpManager');
    const empSignUpBtn = document.getElementById('signUpEmp');


    //가입 유형별 가입창
    const managerSignUpContainer = document.getElementById('signUpManagerDiv');
    const empSignUpContainer = document.getElementById('signUpEmpDiv');

    //온클릭 이벤트 등록
    managerSignUpBtn.addEventListener('click', function () {
        signUpSelectorContainer.remove();
        managerSignUpContainer.classList.remove('d-none');
        empSignUpContainer.remove();
    });

    empSignUpBtn.addEventListener('click', function () {
        signUpSelectorContainer.remove();
        empSignUpContainer.classList.remove('d-none');
        managerSignUpContainer.remove();
    })
}

init();



























