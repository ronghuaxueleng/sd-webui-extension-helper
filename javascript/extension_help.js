"use strict";

function update_extensions(path) {
    let textarea = gradioApp().querySelector('#extension_path textarea')
    textarea.value = path
    updateInput(textarea)
    textarea.click()
    gradioApp().querySelector('#update_extensions_btn').click()
}

function delete_extensions(path) {
    if (confirm('确定要删除这个扩展吗？')) {
        let textarea = gradioApp().querySelector('#extension_path textarea')
        textarea.value = path
        updateInput(textarea)
        textarea.click()
        gradioApp().querySelector('#delete_extensions_btn').click()
    }
}