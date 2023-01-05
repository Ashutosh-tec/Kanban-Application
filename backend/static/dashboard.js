const store = new Vuex.Store({
  strict: true,
    state: {
      lists : []
    },
    
    getters: {
    },
    mutations: {
      addLists(state,data) {
        state.lists = data
        console.log(data)
        console.log(typeof(data))
      }
    },
    actions:{
      async fetchLists(context){
        const res = await fetch("/api/user/lists/1")
        if(res.ok){
          const data = await res.json()
          // console.log(data)
          context.commit('addLists', data)
        }
      }
    }
    
  })

const List_comp = Vue.component('List_card', {
  template: '<div class="component"><h2> {{list_title}} </h2></div>',
      
  data: function() {
    return {
      nclick: 0
    }
  },
     
});

const contents = Vue.component('cont',{
  template: `<div class="main_body">
      
      <div class="card bg-secondary" style="size: 10px; width: max-content; margin: 20px;">
      <div v-for="list in lists" :key="list.list_id">
      
        <div class="card-header">
            <b>{{list.list_name}}</b>  <br>
            <div class="dropdown">
                <button>List Options</button>
                <div class="dropdown-content">
                <a href="/todos/#">Edit</a>
                <a href="/todos/#">Delete</a>
                </div>
              </div>
            <br>
            <br><br>
        </div>
      </div>
      </div>
          </div>`,
  computed:{
    lists(){
      return this.$store.state.lists
    }
  }
})


var app = new Vue({
  el: '#app',
  store: store,
  components: {
 List_comp,
 contents
  },
    
    // router: router,
    
    // props:[user_name],
    created: function(){
      this.$store.dispatch('fetchLists')
        // console.log("Hello", user_name)
    }
})