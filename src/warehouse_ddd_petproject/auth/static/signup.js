function checkPasswords() {
  const isValid = password.checkValidity();
  const isEqual = password.value === passwordConfirm.value;

  if (!isValid || !isEqual) {
    passwordConfirm.setCustomValidity("Passwords don't match");
    button.setAttribute("disabled", "disabled");
  } else {
    passwordConfirm.setCustomValidity("");
    button.removeAttribute("disabled");
  }
}

const [password, passwordConfirm] = document.querySelectorAll(
  "input[type=password]"
);

const button = document.querySelector("form button");

Array.of(password, passwordConfirm).forEach((el) => {
  el.addEventListener("input", checkPasswords);
});
