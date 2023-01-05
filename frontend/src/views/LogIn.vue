<template>
  <div class="root">
    <h3>LOG IN PAGE</h3>
    <form action="">
      <div class="container">
        <label for="uname"><b>Email</b></label>
        <input
          type="text"
          placeholder="Enter Email"
          name="email"
          v-model="formData.email"
          required
        />
        <br />
        <label for="psw"><b>Password </b> </label>
        <input
          type="password"
          placeholder="Enter Password"
          name="psw"
          v-model="formData.password"
          required
        />
        <br />
      </div>

      <div>
        <!-- <button type="submit" value="submit" style="font-size: 28px;" href=log_in_page.html>Login</button> -->
        <button @click.prevent="loginMethod" style="font-size: 28px">
          Login
        </button>
      </div>
      <div class="container" style="background-color: #f1f1f1; font-size: 20px">
        <span class="others">
          <a href="/" style="size: 10px">Create an account</a>
        </span>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "LogIn",
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    // setCookie(cname, cvalue, exdays) { //This methode use to set cookie in case
    //   const d = new Date();
    //   d.setTime(d.getTime() + (exdays*24*60*60*1000));
    //   let expires = "expires="+ d.toUTCString();
    //   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    // },
    async loginMethod() {
      const res = await fetch(
        "http://127.0.0.1:5000/login?include_auth_token",
        {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.formData),
        }
      );

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem(
          "auth-token",
          data.response.user.authentication_token
        );
        const res2 = await fetch(
          `http://127.0.0.1:5000/api/user/${this.formData.email}`,
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );
        if (res2.ok) {
          const data = await res2.json();
          console.log(data);
          localStorage.setItem("user_id", data.id);
          localStorage.setItem("username", data.username);
        }
        this.$router.push("/");
        // console.log(data)
      } else {
        console.log("something went wrong");
      }
    },
  },
};
</script>

<style>
/* Bordered form */
form {
  border: 3px solid #f1f1f1;
}

/* Full-width inputs */
input[type="text"] {
  width: 80%;
  padding: 12px 20px;
  margin: 8px 25px;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

input[type="password"] {
  width: 80%;
  padding: 12px 20px;
  margin: 8px 25px;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Set a style for all buttons */

/* Add a hover effect for buttons */
button:hover {
  opacity: 0.8;
}

/* Extra style for the cancel button (red) */
.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

/* Add padding to containers */
.container {
  padding: 16px;
}

/* The "Forgot password" text */
span.others {
  float: right;
  padding-top: 16px;
  opacity: 0.8;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
}
</style>
