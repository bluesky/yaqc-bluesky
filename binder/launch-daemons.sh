yaqd-fake-continuous-hardware --config ${REPO_DIR}/binder/fake-continuous-hardware-config.toml &>/dev/null &
python -c "import yaqc; c = yaqc.Client(38100); c.set_position(0)"
python -c "import yaqc; c = yaqc.Client(38101); c.set_position(0)"
python -c "import yaqc; c = yaqc.Client(38102); c.set_position(0)"
yaqd-fake-triggered-sensor --config ${REPO_DIR}/binder/fake-triggered-sensor-config.toml &>/dev/null &
disown
