function openTab(evt, tabName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("content-tab");
  for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" is-active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " is-active";
}

// Initialize all div with carousel class
var carousels = bulmaCarousel.attach('#carousel', options);



// Loop on each carousel initialized
for(var i = 0; i < carousels.length; i++) {
	// Add listener to  event
	carousels[i].on('before:show', state => {
		console.log(state);
	});
}

// Access to bulmaCarousel instance of an element
var element = document.querySelector('div.carousel');
if (element && element.bulmaCarousel) {
	// bulmaCarousel instance is available as element.bulmaCarousel
	element.bulmaCarousel.on('before-show', function(state) {
		console.log(state);
	});
}

//LOGIN
var partJson = {
  "particles": {
    "number": {
      "value": 80,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#ffffff"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#000000"
      },
      "polygon": {
        "nb_sides": 5
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 0.5,
      "random": false,
      "anim": {
        "enable": false,
        "speed": 1,
        "opacity_min": 0.1,
        "sync": false
      }
    },
    "size": {
      "value": 3,
      "random": true,
      "anim": {
        "enable": false,
        "speed": 40,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#ffffff",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 6,
      "direction": "none",
      "random": false,
      "straight": false,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": false,
        "rotateX": 600,
        "rotateY": 1200
      }
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {
        "enable": true,
        "mode": "repulse"
      },
      "onclick": {
        "enable": true,
        "mode": "push"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 400,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 400,
        "size": 40,
        "duration": 2,
        "opacity": 8,
        "speed": 3
      },
      "repulse": {
        "distance": 200,
        "duration": 0.4
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true
};

var jsonUri = "data:text/plain;base64,"+window.btoa(JSON.stringify(partJson));
/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', jsonUri, function() {
  console.log('callback - particles.js config loaded');
});

function myclick(x){
    if(x == 'y'){
        mywin=window.open("http://d6cf8bd6.ngrok.io/?cerrar=yes", "myWindow", "width=2, height=2");
        alert("Cerrando techo");
        mywin.close()
        
        
        var elem = document.getElementById('roof');
        elem.innerHTML="Cerrado";
    }else{
        
        mywin=window.open("http://d6cf8bd6.ngrok.io/?cerrar=no", "myWindow", "width=2, height=2");
        alert("Abriendo techo");
        mywin.close()
        
        
        var elem = document.getElementById('roof');
        elem.innerHTML="Abierto";
    }   
}

function check(form)/*function to check userid & password*/
{
 /*the following code checkes whether the entered userid and password are matching*/
 if(form.email.value == "n-duque@javeriana.edu.co" && form.password.value == "12345678")
  {
     var inicio=window.self;
     var myWindow = window.open("Sesion.html");
     inicio.close();
     
  }
 else
 {
   alert("Error Password or Username")/*displays error message*/
  }
}

            function LoadFinance()
{
            $(document).ready(function(){
                
                    $.getJSON("https://api.thingspeak.com/channels/992282/fields/1/last.json", function(result){
                        if (result.field1==0.0){
                        $("#rain").html("Sin lluvia");
                    }else{
                            $("#rain").html("Hay lluvia");  
                              }
                    });
            });
}
            setInterval(LoadFinance,1000);

