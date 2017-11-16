Vue.component('studentslist', {
  template: `<div id='studentContainer'>
      <alum-row
      v-for="row in rows"
      :key='rows.indexOf(row)'
      :students='rows[rows.indexOf(row)]'></alum-row>
    </div>`,
  data: function() {return {
    students: [],
    rows: []
  }},
  created: function() {
    // call database
    axios.get(`http://local.ericmschow.com:8888/api/`)
      .then((response) => {
        this.getRows(response.data)
      })
  },
  methods: {
    getStudent: function() {
      let stud = this.students.shift();
      return stud ? stud : null
    },
    getRows: function(students) {
      this.students = students
      // round up since we need a row even if not full
      let totalRows = Math.ceil(students.length/3);
      // console.log('getting rows: total ', total)
      for (let i = 0; i < totalRows; i++){
        let row = []
        // only add students to row if they exist
        let stud0 = this.getStudent()
        console.log('stud0 is ', stud0)
        if (stud0 !== null) {
          row.push(stud0)
          let stud1 = this.getStudent()
          console.log('stud1 is ', stud1)
          if (stud1 !== null) {
            row.push(stud1)
            let stud2 = this.getStudent()
            console.log('stud2 is ', stud2)
            if (stud2 !== null){
              row.push(stud2)
            }
          }
        }
        this.rows.push(row)
        console.log('rows are ', this.rows)
      }
    }
  }
})
Vue.component('alum-row', {
  template: `<div class='row alum-row'>
    <alum-container
    v-for='student, index in students'
    :student=student
    :arrlength=arrlength
		:index=index
    ></alum-container>
    </div>`,
  // data: function() {return {students: this.students}},
  props: {students: Array},
  computed: {
    arrlength: function() {console.log('arrlength computered'); return Number(this.students.length)}
  },
  created: function() {
    console.log('row created, computed ', this.arrlength)
  }
})
Vue.component('alum-container', {
	template: `<div :class="columnClassVar ">
		<alum :student=student>
		</alum>
	</div>`,
	props: {student: Object, arrlength: Number, index: Number },
	computed: {columnClassVar: function() {
			if (this.arrlength === 3) {
				// console.log('arr 3')
				return "col-sm-4 col-xs-12 alum-container"
			}
			else if (this.arrlength === 2) {
				if (this.index === 0) {
					// console.log('arr 2 0')
					return "col-sm-4 col-sm-offset-2 col-xs-12 alum-container"
				} else if (this.index === 1) {
					// console.log('arr 2 1')
					return "col-sm-4 col-xs-12 alum-container"
				} else {
					console.error('arrlength 2 not getting index')
				}
			} else if (this.arrlength === 1) {
				// console.log('arr 1')
				return "col-sm-4 col-sm-offset-4 col-xs-12 alum-container"
			} else {console.error('columnClassVar compute not getting arrlength', this.arrlength)}
		}
	}
})
Vue.component('alum', {
  template: `
<div class='alum'>
  <h4>{{student.fname.toUpperCase()}} {{student.lname.toUpperCase()}}</h4>
  <h6>{{student.tag.toUpperCase()}}</h6>
  <hr class='green1'>
  <p>{{student.description}}</p>
  <hr class='green1'>
  <div class='row icons'>
    <a :title=githubtitle :href=github target="_blank"><i class="fa fa-github" aria-hidden="true"></i></a>
    <a :title=linkedintitle :href=linkedin target="_blank"><i class="fa fa-linkedin" aria-hidden="true"></i></a>
    <a :title=resumetitle :href=resume target="_blank"><i class="fa fa-file-text-o" aria-hidden="true"></i></a>
    <a :title=portfoliotitle :href=portfolio target="_blank"><i class="fa fa-file-code-o" aria-hidden="true"></i></a>
  </div>
</div>`,
  props: {student: Object, arrlength: Number },
	// data() {return {student: this.student, arrlength: this.arrlength}},
  created: function() {
    console.log('alum created', this.student, this.arrlength)
  },
  computed: {
    github: function() {
      return (this.student.github)
    },
    linkedin: function() {
      return (this.student.linkedin)
    },
    resume: function() {
      return (this.student.resume)
    },
    portfolio: function() {
      return (this.student.portfolio)
    },
    githubtitle: function() {
      return ('' + this.student.name + "'s GitHub Account")
    },
    linkedintitle: function() {
      return ('' + this.student.name + "'s LinkedIn Account")
    },
    resumetitle: function() {
      return ('' + this.student.name + "'s Resume")
    },
    portfoliotitle: function() {
      return ('' + this.student.name + "'s Personal Website and Portfolio")
    }
  }
})

const app = new Vue({
  el: '#app',
	components: {"navbar": navbar}
})
