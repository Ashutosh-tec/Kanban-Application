<template>
  <div class="root">
    <div class="headers">
      <h1><u>Welcome to KANBAN APP</u></h1>
      <h3>Please creatre your account to track your tasks.</h3>
    </div>
    <div style="width: 75%">
      <b-form
        @submit="onSubmit"
        @reset="onReset"
        v-if="show"
        style="margin-left: 2rem"
      >
        <b-form-group
          id="input-group-1"
          label="Email address:"
          label-for="input-1"
          description="We'll never share your email with anyone else."
        >
          <b-form-input
            id="input-1"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
            style="width:70%; margin:1.2em"
          ></b-form-input>
        </b-form-group>
        <br/>
        <b-form-group id="input-group-2" label="User Name:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.username"
            placeholder="Enter name"
            required
            style="width:70%;"
          ></b-form-input>
        </b-form-group>


        <b-form @submit.stop.prevent>
          <label for="text-password">Password:</label>
          <br/>
          <b-form-input
            type="password"
            id="text-password"
            v-model="form.password"
            aria-describedby="password-help-block"
            required
            style="width:70%;"
          ></b-form-input>
          
          <b-form-text id="password-help-block">
            Your password must be 8-20 characters long,
          </b-form-text>
        </b-form>

        <!-- <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
          <b-form-checkbox-group
            v-model="form.checked"
            id="checkboxes-4"
            :aria-describedby="ariaDescribedby"
          >
            <b-form-checkbox value="me">Check me out</b-form-checkbox>
            <b-form-checkbox value="that">Check that out</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group> -->

        <b-button type="submit" variant="primary" style="margin:1rem">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
      <!-- <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card> -->
      <div class="alter" style="float:right">
        <p>Already have an account <a href="/login">LogIn</a></p>
      </div>
    </div>
  </div>
</template>

<script>
// import { text } from 'body-parser';

export default {
  name: 'create_account',
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
      },

      show: true,
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      if (this.form.password.length < 8 || this.form.password.length > 20) {
        alert("Your Password should contain 8-20 characters.");
      } else if (this.form.email.includes(".")) {
        event.preventDefault();
        // alert(JSON.stringify(this.form));
        try {
          console.log(JSON.stringify(this.form));
          const res = await fetch("http://127.0.0.1:5000/api/adduser", {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
          });
          if (res.ok) {
            alert("Please Log in with these credential.")
            this.$router.push("/login");
          }
        } catch (e) {
          // event.preventDefault();
          console.log(e);
        }
      } else {
        alert("There is something wrong in Email address.");
      }
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.username = "";
      this.form.password = "";
      // Trick to reset/clear native browser form validation state

    //   this.$nextTick(() => {
    //     this.show = true;
    //   });
    },
  },
};
</script>
<style scoped>
.headers {
  text-align: center;
}
</style>
