function signin(identity, password) {
  $.get("/rsa/public.key",
        function(result) {
          var pub = result;
          var pubkey = new RSAKey();
          pubkey.setPublic(pub, '10001');
          identity = pubkey.encrypt(identity);
          password = pubkey.encrypt(password);

          $.ajax({
            url:"/api/signin", 
            data: {"identity": identity,
                   "password": password
            }, 
            success: function(data) {
              alert(data);
            },
            error: function(jqXHR, status, exception) {
              alert(exception);
            }
          });
        });
}
