const showToast = (message, isError = false) => {
  Toastify({
    text: message,
    duration: 3000,
    gravity: "top",
    position: "right",
    backgroundColor: isError ? "#dc3545" : "#28a745",
  }).showToast();
};

export default showToast;
