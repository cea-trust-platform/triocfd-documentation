const animateBackground = [
    { background: "red" },
    { background: "none" },
  ];
  
  const animateTiming = {
    duration: 2000,
    iterations: 1,
  };

function setfocus(){
    let loc=window.location

    let hash=loc.hash.substring(1)
    // console.log(hash)
    let elem=document.getElementById(hash)
    if (elem){
        // console.log(elem)
        elem.animate(animateBackground,animateTiming)
    }

}

_ready(function() {
    setfocus();
    window.addEventListener("hashchange", (event) => { setfocus()});
});

