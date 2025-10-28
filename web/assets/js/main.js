(function(){
  // Simple contact form handler
  const form = document.getElementById('contact-form');
  if(form){
    const hint = document.getElementById('form-hint');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!form.checkValidity()){
        hint.textContent = '请完整填写必填项并同意隐私政策。';
        hint.style.color = '#FF4D4D';
        return;
      }
      hint.textContent = '提交成功！我们会在 24 小时内与您联系。';
      hint.style.color = '#18C4B8';
      form.reset();
    });
  }
})();


