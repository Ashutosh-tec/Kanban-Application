<template>
  <div class="root">
    <NavBar />
    <h1>Provide the list details</h1>
    <form action="">
      <div class="container">
        <label for="lstname"><b>List Name </b></label>
        <input
          type="text"
          placeholder="Enter here"
          name="text"
          v-model="formData.list_name"
          required
        />
        <br />
        <label for="lstdescr"><b>List Description </b> </label>
        <input
          type="text"
          placeholder="Write a brief description here"
          name="description"
          v-model="formData.list_description"
        />
        <br />
      </div>

      <div>
        <button @click.prevent="addList" style="font-size: 28px">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "Add_List",
  data() {
    return {
      formData: {
        list_name: "",
        list_description: "",
        user_id : localStorage.getItem("user_id")
      },
    };
  },
  components: {
    NavBar,
  },
  methods: {
    async addList() {
      if (this.formData.list_name != "") {
        const res = await fetch(
          "http://127.0.0.1:5000/api/user/add_list",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
            body: JSON.stringify(this.formData),
          }
        );
        if (res.ok){
            this.$router.push("/");
        }
      }
      else{
        alert("List name is essential.")
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
