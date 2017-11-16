Vue.component('navbar', {
  template: `
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand centered" target="_blank" href="https://www.digitalcrafts.com">
            <img src="/static/img/DigitalCrafts-Logo-Wrench.png"
            alt='DigitalCrafts wrench logo'
            width="45px">
          </a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav navbar-right">
            <li><a id="registryLink" href="/">View Current Job Seekers</a></li>
            <li><a href="mailto:hello@digitalcrafts.com">Email DigitalCrafts</a></li>
            <li><a href="/profile">Student Profile</a></li>
            
            <!--
            <li><a href="/logout">Logout</a></li>

              UNCOMMENT HERE TO REENABLE LOGOUT
              need to refactor html serving to enable checking for login,
              or find a way for Vue to check for the secure cookie -->
          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>`
})

const navbar = new Vue({
  el: 'navbar'
})
