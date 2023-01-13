<template>
  <div class="root">
    <h3>LOG IN PAGE</h3>
    




    <b-form @submit="loginMethod">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="formData.email"
          type="email"
          placeholder="Enter email"
          required
          style="width:70%; margin:1.2em"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Password:" label-for="input-1">
        
        <b-form-input
          type="password"
          id="input-1"
          v-model="formData.password"
          style="width:70%"
          required
        ></b-form-input>
        
        <b-form-text id="password-help-block">
          Your password must be 8-20 characters long,
        </b-form-text>
      </b-form-group>

      

      <b-button type="submit" variant="primary">Submit</b-button>

    </b-form>
    <div class="container" style="background-color: #f1f1f1; font-size: 20px">
      <span class="others">
        <a href="/create_account" style="size: 10px">Create an account</a>
      </span>
    </div>





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
    async loginMethod(event) {
      event.preventDefault()
      try{
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
        alert("Your Email or Password is wrong. Please check once again.");
      }
      } catch(e){
        console.log(e)
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
