const verticalMenu = document.querySelector(".vertical-menu")

function createLink(href, linkText){
    let aLink = document.createElement("A")
    aLink.setAttribute("href", href)
    aText = document.createTextNode(linkText)
    aLink.append(aText)
    return aLink
}

verticalMenu.appendChild(createLink("linux_intro.html","1. Linux Introduction"))
verticalMenu.appendChild(createLink("python_intro.html","2. Python Introduction"))
verticalMenu.appendChild(createLink("variables_data_types.html","3. Variables and Data Types"))
verticalMenu.appendChild(createLink("compound_data_types.html","4. Compound Data Types"))
verticalMenu.appendChild(createLink("control_structures.html","5. Control Structures"))
verticalMenu.appendChild(createLink("functions.html","6. Functions"))
verticalMenu.appendChild(createLink("exceptions.html","7. Exceptions"))
verticalMenu.appendChild(createLink("#","8. Object Orientation"))
verticalMenu.appendChild(createLink("modules_packages.html","9. Modules and Packages"))
verticalMenu.appendChild(createLink("homework.html#","* Homework exercises"))
