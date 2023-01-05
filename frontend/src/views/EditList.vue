<template>
  <div class="root">
    <NavBar />
    <h1>Edit Your List</h1>
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
        <button @click.prevent="editList" style="font-size: 28px">
          Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "Edit_List",
  
  components: {
    NavBar
  },
  data() {
    return {
      formData: {
        list_name: "",
        list_description: ""
      },
      
    };
  },
  methods: {
      
      async getList(){
          try {
          const res = await fetch(`http://127.0.0.1:5000/api/user/lists/${localStorage.getItem("user_id")}`,{
              headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': localStorage.getItem('auth-token'),
              }
          })
          if (res.ok){
              const data = await res.json()
              this.formData = data.find(
                      (ele) => ele.list_id == this.$route.params.id
                  )
          }
          
          }
          catch (e) {
              console.log(e);
          }
      },
    async editList() {
      try {
      this.formData.user_id = localStorage.getItem("user_id");
      const res = await fetch(
        `http://127.0.0.1:5000/api/user/lists/${this.$route.params.id}`,
        {
          method: "put",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: JSON.stringify(this.formData),
        }
      );
      if (res.ok) {
        this.$router.push("/");
      }

      } catch (e) {
        console.log(e);
      }
    },
  },
  created(){
    this.getList();
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
