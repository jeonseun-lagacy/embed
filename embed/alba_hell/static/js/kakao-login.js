Kakao.init('6e28e705b856002d4f093f76f3388894');

//카카오 로그인 버튼 생성
Kakao.Auth.createLoginButton({
  container: '#kakaoLogin',
  success: function(response) {
    console.log(response);
  },
  fail: function(error) {
    console.log(error);
  },
});
