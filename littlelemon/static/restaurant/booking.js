(() => {
  const dateInput = document.getElementById("reservation_date");
  const slotSelect = document.getElementById("reservation_slot");
  const bookingList = document.getElementById("booking-list");
  const noBookings = document.getElementById("no-bookings");
  const loading = document.getElementById("loading-message");
  const selectedDate = document.getElementById("selected-date");
  const slotMessage = document.getElementById("slot-message");
  if (!dateInput || !slotSelect) return;

  const originalOptions = Array.from(slotSelect.options).map(option => ({
    value: option.value, text: option.text
  }));

  async function refreshBookings() {
    const selected = dateInput.value;
    selectedDate.textContent = selected || "—";
    loading.hidden = false;
    loading.textContent = "Loading bookings…";
    bookingList.replaceChildren();
    noBookings.hidden = true;
    slotMessage.textContent = "";

    if (!selected) {
      loading.hidden = true;
      return;
    }

    try {
      const response = await fetch(`/bookings?date=${encodeURIComponent(selected)}`, {
        headers: { "Accept": "application/json" }
      });
      if (!response.ok) throw new Error("Could not retrieve bookings.");
      const bookings = await response.json();
      const bookedSlots = new Set(bookings.map(booking => String(booking.reservation_slot)));

      const currentValue = slotSelect.value;
      slotSelect.replaceChildren();
      originalOptions.forEach(item => {
        const option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.text;
        if (bookedSlots.has(item.value)) {
          option.disabled = true;
          option.textContent += " — Booked";
        }
        slotSelect.appendChild(option);
      });
      if (currentValue && !bookedSlots.has(currentValue)) slotSelect.value = currentValue;
      else {
        const firstAvailable = Array.from(slotSelect.options).find(option => option.value && !option.disabled);
        if (firstAvailable) slotSelect.value = firstAvailable.value;
      }

      bookings.forEach(booking => {
        const li = document.createElement("li");
        li.textContent = `${booking.first_name} - ${booking.reservation_time}`;
        bookingList.appendChild(li);
      });
      noBookings.hidden = bookings.length !== 0;
      loading.hidden = true;
      if (bookedSlots.size === originalOptions.length - 1) {
        slotMessage.textContent = "All reservation times are booked for this date.";
      }
    } catch (error) {
      loading.hidden = false;
      loading.textContent = "Unable to load bookings. Please refresh the page.";
    }
  }

  dateInput.addEventListener("change", refreshBookings);
  refreshBookings();
})();
