(() => {
  const output = document.getElementById("reservations-json");
  if (!output) return;
  fetch("/bookings", { headers: { "Accept": "application/json" } })
    .then(response => {
      if (!response.ok) throw new Error("Request failed");
      return response.json();
    })
    .then(data => {
      output.textContent = JSON.stringify(data, null, 2);
    })
    .catch(() => {
      output.textContent = "Unable to load reservations. Check the server and database configuration.";
    });
})();
