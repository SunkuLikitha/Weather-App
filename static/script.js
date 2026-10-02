const weatherForm = document.querySelector("#weather-form");
const cityInput = document.querySelector("#city-input");
const formMessage = document.querySelector("#form-message");
const weatherCard = document.querySelector("#weather-card");
const weatherIcons = {
    sun: [0x2600, 0xfe0f],
    moon: [0x1f319],
    "partly-cloudy": [0x26c5],
    cloud: [0x2601, 0xfe0f],
    fog: [0x1f32b, 0xfe0f],
    drizzle: [0x1f326, 0xfe0f],
    rain: [0x1f327, 0xfe0f],
    snow: [0x1f328, 0xfe0f],
    thunderstorm: [0x26c8, 0xfe0f],
};

function showMessage(message, state = "error") {
    formMessage.textContent = message;
    formMessage.dataset.state = state;
}

function displayWeather(weather) {
    document.querySelector("#city-name").textContent = `${weather.city}, ${weather.country}`;
    document.querySelector("#condition").textContent = weather.condition;
    document.querySelector("#temperature").textContent = weather.temperature;
    document.querySelector("#feels-like").textContent = weather.feels_like;
    document.querySelector("#humidity").textContent = weather.humidity;
    document.querySelector("#wind-speed").textContent = weather.wind_speed;
    document.querySelector("#pressure").textContent = weather.pressure;

    const icon = document.querySelector("#weather-icon");
    icon.textContent = String.fromCodePoint(...(weatherIcons[weather.icon] || weatherIcons.cloud));
    icon.setAttribute("aria-label", weather.condition);
    weatherCard.hidden = false;
}

weatherForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const city = cityInput.value.trim();

    if (!city) {
        showMessage("Please enter a city name.");
        cityInput.focus();
        return;
    }

    showMessage("Looking up the latest weather...", "loading");
    weatherForm.querySelector("button").disabled = true;

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        let result;

        try {
            result = await response.json();
        } catch {
            throw new Error("The weather server returned an invalid response. Please try again.");
        }

        if (!response.ok) {
            throw new Error(result.error || "The weather server returned an error. Please try again.");
        }

        displayWeather(result);
        showMessage("");
    } catch (error) {
        const message = error instanceof TypeError
            ? "Could not reach the weather server. Check your connection and try again."
            : error.message || "The weather server is unavailable. Please try again.";
        showMessage(message);
    } finally {
        weatherForm.querySelector("button").disabled = false;
    }
});