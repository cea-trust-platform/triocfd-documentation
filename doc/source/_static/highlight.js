const animateBackground = [
    {
        background: "#af0d0db6"
     },
    {
        background: "none"
    },
  ];
  
  const animateTiming = {
    duration: 2500,
    iterations: 1,
  };


var prev_highlight_elem=null;
var prev_highlight_props=null;

function setfocus(){
    let loc=window.location

    let hash=loc.hash.substring(1)
    // console.log(hash)
    let elem=document.getElementById(hash)
    if (elem){
        
        // this highlights by setting a background that slwoy returns to normal. kinda flashy 
        // elem.animate(animateBackground,animateTiming)


        // this sets a permanent left border to highlight
        let len="6px"
        let color="#b80000de"
        let props={
          borderLeftStyle: "solid",
          borderLeftWidth: len,
          borderLeftColor: color,
          paddingLeft: len,

          // borderRightStyle: "solid",
          // borderRightWidth: len,
          // borderRightColor: color,
          // paddingRight: len,
        }

        // reset props of previously highlighted item
        if (prev_highlight_elem){
          for (let [prop, val] of Object.entries(props)){
            prev_highlight_elem.style[prop]=prev_highlight_props[prop]
          }
        }

        // store props of new highlighted item and update them
        prev_highlight_elem=elem
        prev_highlight_props={}

        for (let [prop, val] of Object.entries(props)){
          prev_highlight_props[prop]=elem.style[prop]
          elem.style[prop]=val
        }

    }

    // TODO : if empty elem, find next nonempty (for cases where we have multiple targets using empty span elements for id location)

}

_ready(function() {
    setfocus();
    window.addEventListener("hashchange", (event) => { setfocus()});
});

