const searchInput = document.querySelector("[data-search]")

let file = []
file ='{{files}}'
console.log(file);

searchInput.addEventListener("input", (e) => {
    const value = e.target.value.toLowerCase()
    console.log(value);
    // files.forEach(file => {
    //   const isVisible =
    //     file.name.toLowerCase().includes(value) ||
    //     file.created_at.toLowerCase().includes(value)
    //   file.element.classList.toggle("hide", !isVisible)
    // })
  })
