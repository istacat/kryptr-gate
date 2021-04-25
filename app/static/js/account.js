document.addEventListener('DOMContentLoaded', function () {
  const editForm = document.querySelector('.edit__form');
  if (editForm) {
    const gif = document.querySelector('#gif');
    const submitButton = document.querySelector('#sub');
    if(gif) {
      editForm.addEventListener('submit', function(e){
        gif.style.visibility = 'visible';
        gif.style.height = '100%';
        submitButton.disabled = true;
      });
    }
  }
});
