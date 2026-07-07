document.addEventListener('DOMContentLoaded', function () {
  const passwordInput = document.getElementById('id_password');
  const toggleButton = document.getElementById('togglePassword');
  const form = document.getElementById('loginForm');
  const submitButton = document.getElementById('loginButton');

  if (toggleButton && passwordInput) {
    toggleButton.addEventListener('click', function () {
      const isPassword = passwordInput.type === 'password';
      passwordInput.type = isPassword ? 'text' : 'password';
      toggleButton.innerHTML = isPassword ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
    });
  }

  if (form && submitButton) {
    form.addEventListener('submit', function () {
      submitButton.disabled = true;
      submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Signing in...';
    });
  }
});
