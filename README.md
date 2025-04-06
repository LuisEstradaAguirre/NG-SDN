# NG-SDN

This project leverages the **NG-SDN Framework**, which is composed of:

- [ONOS](https://onosproject.org/)
- [Stratum](https://opennetworking.org/stratum/)
- [P4 Language](https://p4.org/)

## How to Use

The project includes three Docker containers:

1. **ONOS Controller**  
2. **Mininet with Stratum Switches**  
3. **ONOS CLI**

---

## How to Start

### 1. Start the ONOS Controller (in a separate terminal)

make controller

Make sure ONOS has fully started before continuing.

---

### 2. Start Mininet with Stratum (in another terminal)

make mininet

---

### 3. Apply the Network Configuration
make netcfg

---

### 4. Activate the Forwarding App in ONOS CLI (in another terminal)

```bash
make cli
