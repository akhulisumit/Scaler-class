function calculateArea(radius) {
    return 3.14 * radius * radius
}

function calculateCircumference(radius) {
    return 2 * 3.14 * radius
}

function calculateDiameter(radius) {
    return 2 * radius
}

let radius = [1, 2, 3, 3, 5]

function data(radius, cb) {
    let data = []
    for(let i = 0; i < radius.length; i++) {
        data.push(cb(radius[i]))
    }
    return data
}

let areas = data(radius, calculateArea)
console.log(areas)
let circumferences = data(radius, calculateCircumference)
console.log(circumferences)
let diameters = data(radius, calculateDiameter)
console.log(diameters)

