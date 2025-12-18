const temp_re = /T0:(.*) T1:(.*) B:(.*)\r\n/;
//there is some data here I ignore.
const status_re = /CurrentFile: (.*)\r\n/;
const progress_re = /byte (\S\w*)\/(\S\w*)\r\nLayer: (\S\w*)\/(\S\w*)/;

let printer_ip = "";

if ((printer_ip_match = location.search.match(/[&?]printer-ip=([^&]+)/))) {
  printer_ip = printer_ip_match[1];
  document.getElementById("stream").src =
    `http://${printer_ip}:8080/?action=stream`;
  console.log(printer_ip);
}

const slider = document.getElementById("slider");

let interval = setInterval(() => {
  fill_data();
}, slider.value);

console.log(slider);
slider.addEventListener("change", (e) => {
  fill_data();

  let value = e.target.value;

  clearInterval(interval);

  if (value > 0) {
    interval = setInterval(() => {
      fill_data();
    }, value);
  } else {
    interval = 0;
    // show button
  }
  console.log(updateInterval);
});

slider.addEventListener("input", (e) => {
  const seconds = e.target.value / 1000;
  document.getElementById("sliderLabel").innerText =
    `${seconds} second${seconds == 1 ? "" : "s"}`;

  if (seconds == 0) {
    document.getElementById("sliderLabel").style.display = "none";
    document.getElementById("updateButton").style.display = "flex";
  } else {
    document.getElementById("sliderLabel").style.display = "flex";
    document.getElementById("updateButton").style.display = "none";
  }
});

const fill_data = () => {
  fetch(`./temp?printer-ip=${printer_ip}`)
    .then((resp) => {
      if (resp.status === 503) {
        document.getElementById("disconnected-message").style.display = "flex";
        document.getElementById("slider").value = 0;
        document.getElementById("sliderLabel").innerText = "0 seconds";
        document.getElementById("sliderLabel").style.display = "none";
        document.getElementById("updateButton").style.display = "flex";
        if (interval !== 0) {
          clearInterval(interval);
        }
        interval = 0;
      }
      return resp.text();
    })
    .then((text) => {
      const temp_match = text.match(temp_re);

      document.getElementById("temp0").textContent = temp_match[1];
      document.getElementById("temp1").textContent = temp_match[3];
    })
    .catch((e) => {});

  fetch(`./status?printer-ip=${printer_ip}`)
    .then((resp) => resp.text())
    .then((text) => {
      const status_match = text.match(status_re);

      document.getElementById("file").textContent = status_match[1];
    })
    .catch((e) => {});
  fetch(`./progress?printer-ip=${printer_ip}`)
    .then((resp) => resp.text())
    .then((text) => {
      const progress_match = text.match(progress_re);

      let [_, a, b, c, d] = progress_match;
      document.getElementById("byte-progress").value = a;
      document.getElementById("byte-progress").max = b;
      document.getElementById("byte-progress-text").textContent = `${a}/${b}`;

      document.getElementById("layer-progress").value = c;
      document.getElementById("layer-progress").max = d;
      document.getElementById("layer-progress-text").textContent = `${c}/${d}`;
    })
    .catch((e) => {});
};

fill_data();

updateInterval = 0;

const toggle_light = async () => {
  await fetch(`./light_on?printer-ip=${printer_ip}`).catch((e) => {});
};

pause_alert = document.getElementById("pause-alert");
pause_confirm = document.getElementById("pause-confirm");

const pause = async () => {
  pause_alert.show();
};

pause_alert.addEventListener("close", () => {
  if (pause_alert.returnValue == "ok") {
    fetch(`./pause?printer-ip=${printer_ip}`)
      .then((resp) => {
        setTimeout(() => {
          pause_confirm.close();
        }, 2000);
        pause_confirm.show();
      })
      .catch((e) => {
        document.getElementById("pause-confirm-form").innerText =
          "Couldn't send pause signal.";
        pause_confirm.show();
      });
  }
});

document.getElementById("ip-input").value = printer_ip;

refreshbutton = () => {
  let link = window.location.href;

  if ((w = link.indexOf("?")) != -1) {
    link = link.slice(0, w);
  }
  window.location.href = `${link}?printer-ip=${document.getElementById("ip-input").value}`;
};

const image_error = () => {
  document.getElementById("image-error-message").style.display = "flex";
};

const retry_camera = async () => {
  document.getElementById("stream").src =
    `http://${printer_ip}:8080/?action=stream&cachebreaker=${new Date().getTime()}`;
  document.getElementById("image-error-message").style.display = "none";
};

const hide_camera = () => {
  document.getElementById("image-error-message").style.display = "none";
  document.getElementById("stream").style.display = "none";
};
