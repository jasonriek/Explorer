const command_span = document.getElementById('command');   
  const haveEvents = 'ongamepadconnected' in window;
  const controllers = {};
  let debounceTimeout = null;

  function connecthandler(e) {
      addgamepad(e.gamepad);
  }

  function addgamepad(gamepad) {
      controllers[gamepad.index] = gamepad;

      const d = document.createElement("div");
      d.setAttribute("id", `controller${gamepad.index}`);

      const t = document.createElement("h1");
      t.textContent = `gamepad: ${gamepad.id}`;
      d.appendChild(t);

      const b = document.createElement("ul");
      b.className = "buttons";
      gamepad.buttons.forEach((button, i) => {
          const e = document.createElement("li");
          e.className = "button";
          e.textContent = `Button ${i}`;
          b.appendChild(e);
      });

      d.appendChild(b);

      const a = document.createElement("div");
      a.className = "axes";

      gamepad.axes.forEach((axis, i) => {
          const p = document.createElement("progress");
          p.className = "axis";
          p.setAttribute("max", "2");
          p.setAttribute("value", "1");
          p.textContent = i;
          a.appendChild(p);
      });

      d.appendChild(a);

      document.body.appendChild(d);
      requestAnimationFrame(updateStatus);
  }

  function disconnecthandler(e) {
      removegamepad(e.gamepad);
  }

  function removegamepad(gamepad) {
      const d = document.getElementById(`controller${gamepad.index}`);
      document.body.removeChild(d);
      delete controllers[gamepad.index];
  }

  function command(cmd) {
    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }
  
    debounceTimeout = setTimeout(() => {
      fetch(`https://explorer.robot/motor/${cmd}`)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }, 100); // Adjust the delay as needed
  }

  function moveUp() {
      command('forward');
  }

  function moveDown() { 
      command('reverse');
  }

  function moveLeft() {
      command('turn_left');
  }

  function moveRight() {
      command('turn_right');
  }

  function stopMoving() {
      command('stop');
  }

  function updateStatus() {
      if (!haveEvents) {
          scangamepads();
      }

      Object.entries(controllers).forEach(([i, controller]) => {
          const d = document.getElementById(`controller${i}`);
          const buttons = d.getElementsByClassName("button");

          controller.buttons.forEach((button, i) => {
              const b = buttons[i];
              let pressed = button === 1.0;
              let val = button;

              if (typeof button === "object") {
                  pressed = val.pressed;
                  val = val.value;
              }

              const pct = `${Math.round(val * 100)}%`;
              b.style.backgroundSize = `${pct} ${pct}`;
              b.textContent = pressed ? `Button ${i} [PRESSED]` : `Button ${i}`;
              b.className = pressed ? "button pressed" : "button";
              if (i === 1 && pressed) { stopMoving(); }
              else if(i === 12 && pressed) { moveUp(); }
              else if(i === 13 && pressed) {moveDown(); }
              else if(i === 14 && pressed) {moveLeft(); }
              else if(i === 15 && pressed) {moveRight(); }
          });

          const axes = d.getElementsByClassName("axis");
          controller.axes.forEach((axis, i) => {
              const a = axes[i];
              a.textContent = `${i}: ${axis.toFixed(4)}`;
              a.setAttribute("value", axis + 1);
          });
      });

      requestAnimationFrame(updateStatus);
  }

  function scangamepads() {
      const gamepads = navigator.getGamepads();
      const noDevices = document.querySelector("#noDevices");
      noDevices.style.display = gamepads.filter(Boolean).length ? "none" : "block";
      for (const gamepad of gamepads) {
          if (gamepad) {
              if (gamepad.index in controllers) {
                  controllers[gamepad.index] = gamepad;
              } else {
                  addgamepad(gamepad);
              }
          }
      }
  }

  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);

  if (!haveEvents) {
      setInterval(scangamepads, 500);
  }
