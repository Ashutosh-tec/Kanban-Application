<template>
    <!-- <nav class="navbar navbar-expand-md bg-dark navbar-dark">
        <a class="navbar-brand" href="/">KANBAN</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="collapsibleNavbar">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">|</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Summary</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">|</a>
            </li>
            <li class="nav-item">
              <a class="nav-link"
              href=""
              @click.prevent="logout"
              >
                logout
              </a>
              
            </li>    
          </ul>
        </div>  
      </nav> -->



      <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
          <!-- <b-navbar-brand href="#">NavBar</b-navbar-brand> -->
          <div>
            <!-- As a heading -->
            <b-navbar variant="faded" type="light">
              <b-navbar-brand tag="h1" class="mb-0">KANBAN</b-navbar-brand>
            </b-navbar>
          </div>
          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      
          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
              <b-nav-item href="/" >Home</b-nav-item>
              <b-nav-item href="#" >Summary</b-nav-item>
            </b-navbar-nav>
      
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <!-- <b-nav-form>
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
              </b-nav-form> -->
      
              <!-- <b-nav-item-dropdown text="Lang" right>
                <b-dropdown-item href="#">EN</b-dropdown-item>
                <b-dropdown-item href="#">ES</b-dropdown-item>
                <b-dropdown-item href="#">RU</b-dropdown-item>
                <b-dropdown-item href="#">FA</b-dropdown-item>
              </b-nav-item-dropdown> -->
      
              
              <b-nav-item href="#" @click.prevent="logout">Logout</b-nav-item>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </div>
    
</template>

<script>
export default {
    name: 'NavBar',
    methods: {
    async logout() {
      console.log("Clicked")
      const res = await fetch('http://127.0.0.1:5000/logout')
      if (res.ok) {
        localStorage.clear()
        this.$router.push('/login')
      } else {
        console.log('could not logout the user')
        }
      },
    },
}






</script>

<style>
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
#nav {
  padding: 30px;
  text-align: center;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: whitesmoke;
  background: crimson;
  border-radius: .5rem;
}
</style>