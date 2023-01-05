<template>
  <div class="root">
    <NavBar />
    <h1>Edit Task</h1>

    <form action="">
      <div class="container">
        <label for="title"><b>Task Title </b></label>
        <input
          type="text"
          placeholder="Enter title here"
          name="text"
          v-model="formData.task_title"
          required
        />
        <br />
        <label for="taskDesc"><b>Task Content </b> </label>
        <input
          type="text"
          placeholder="Write Content "
          name="description"
          v-model="formData.task_content"
        />
        <br />
        <label for="deadline"><b>Task Deadline </b></label>
        <input
          type="date"
          name="deadline"
          v-model="formData.task_deadline"
          required
        />
        <br />
        <label for="task_completion"><b>Task Status</b></label>
        <input
          type="radio"
          name="complete"
          v-model="formData.task_status"
          value="Completed"
        />Completed
        <input
          type="radio"
          name="pending"
          v-model="formData.task_status"
          value="Pending"
        />Pending<br />
      </div>

      <div>
        <button @click.prevent="editTask" style="font-size: 28px">
          Submit
        </button>
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
          task_title: "",
          task_content : "",
          task_deadline: "",
          task_status: "Pending"
      }
  //     .find(
  //     (ele) => ele.task_id == this.$route.params.id2
  //   ),
    };
  },


  components: {
    NavBar,
  },
  methods: {
    async getTask(){
      try{
        const res = await fetch(`http://127.0.0.1:5000/api/user/lists/tasks/${this.$route.params.id1}`,{
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth-token'),
          }
        })
        if(res.ok){
          const data = await res.json()
          console.log(data)
          this.formData = data.find(
            (ele) => ele.task_id == this.$route.params.id2)
        }
      }catch(e){
        console.log(e)
      }
      
    },
    async editTask() {
      if (this.formData.list_name != "") {
        try{
          // console.log(JSON.stringify(this.formData))
          const res = await fetch(
            `http://127.0.0.1:5000/api/user/lists/tasks/${this.$route.params.id2}`,
            {
              method: "put",
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
        } catch(e){
          console.log(e)
        }
      }
      else{
        alert("List name is essential.")
      }
    },

  },
  created(){
    this.getTask();
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

input[type="date"] {
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
