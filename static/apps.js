let navbar = document.querySelector(".navbar");
let aboutBut = document.querySelector(".aboutbut");

let tl = gsap.timeline();

tl.from(navbar,{
    y:-50,
    duration: 0.5,
    opacity:0,
    stagger:1  
})

tl.from(".tagline",{
    x:-1500,
    duration:1.5,
    opacity:0,
})
tl.from(".pincodes",{
    opacity:0,
    
})

gsap.from(".pg2-content",{
    y: 500,
    duration:1.5,
    opacity:0,
    scrollTrigger:".pg2-content"
})

gsap.from(".search-content",{
    duration:1.5,
    delay:0.7,
    opacity:0,
})

aboutBut.addEventListener("click",()=>{
    gsap.from(".page2",{
        y:500,
        duration:1.2,
    })
})

