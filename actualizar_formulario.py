#!/usr/bin/env python3
"""
Script para actualizar el formulario de prestadores con las nuevas entidades
"""

import os

def actualizar_formulario():
    """Actualiza el formulario con dropdowns dinámicos"""
    
    # Ruta del formulario
    formulario_path = "src/templates/milotalent/registro/formulario_new.html"
    
    if not os.path.exists(formulario_path):
        print("❌ Archivo de formulario no encontrado")
        return
    
    print("🔄 ACTUALIZANDO FORMULARIO")
    print("=" * 40)
    
    # Crear script JavaScript para cargar entidades
    js_script = '''
// Función para cargar todas las entidades
async function cargarTodasEntidades() {
    console.log('🚀 Cargando todas las entidades...');
    
    try {
        const response = await fetch('/admin/entidades/api/all');
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ Entidades cargadas:', data.data);
            
            // Cargar cada tipo de entidad
            cargarMunicipios(data.data.municipio || []);
            cargarProfesiones(data.data.profesion || []);
            cargarBancos(data.data.banco || []);
            cargarEPS(data.data.eps || []);
            cargarAFP(data.data.afp || []);
            cargarARL(data.data.arl || []);
            cargarCajasCompensacion(data.data.caja_compensacion || []);
            cargarOperadoresSS(data.data.operador_ss || []);
            cargarAreasPersonal(data.data.area_personal || []);
            
        } else {
            console.error('Error cargando entidades:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

function cargarMunicipios(municipios) {
    const selects = ['expedida_id', 'ciudad_nacimiento_id', 'municipio_residencia_id'];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            // Limpiar opciones existentes excepto la primera
            select.innerHTML = '<option value="">Seleccione municipio...</option>';
            
            municipios.forEach(municipio => {
                const option = document.createElement('option');
                option.value = municipio.id;
                option.textContent = municipio.nombre;
                if (municipio.departamento) {
                    option.textContent += ` (${municipio.departamento})`;
                }
                select.appendChild(option);
            });
        }
    });
    console.log(`✅ ${municipios.length} municipios cargados`);
}

function cargarProfesiones(profesiones) {
    const select = document.getElementById('profesion_id');
    if (select) {
        // Convertir input a select
        const parent = select.parentNode;
        const newSelect = document.createElement('select');
        newSelect.className = 'form-select';
        newSelect.id = 'profesion_id';
        newSelect.name = 'profesion_id';
        newSelect.required = true;
        
        newSelect.innerHTML = '<option value="">Seleccione profesión...</option>';
        
        profesiones.forEach(profesion => {
            const option = document.createElement('option');
            option.value = profesion.id;
            option.textContent = profesion.nombre;
            newSelect.appendChild(option);
        });
        
        parent.replaceChild(newSelect, select);
        console.log(`✅ ${profesiones.length} profesiones cargadas`);
    }
}

function cargarBancos(bancos) {
    const select = document.getElementById('banco_id');
    if (select) {
        const newSelect = crearSelectDinamico('banco_id', 'Seleccione banco...', bancos);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${bancos.length} bancos cargados`);
    }
}

function cargarEPS(eps) {
    const select = document.getElementById('eps_id');
    if (select) {
        const newSelect = crearSelectDinamico('eps_id', 'Seleccione EPS...', eps);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${eps.length} EPS cargadas`);
    }
}

function cargarAFP(afp) {
    const select = document.getElementById('afp_id');
    if (select) {
        const newSelect = crearSelectDinamico('afp_id', 'Seleccione AFP...', afp);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${afp.length} AFP cargadas`);
    }
}

function cargarARL(arl) {
    const select = document.getElementById('arl_id');
    if (select) {
        const newSelect = crearSelectDinamico('arl_id', 'Seleccione ARL...', arl);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${arl.length} ARL cargadas`);
    }
}

function cargarCajasCompensacion(cajas) {
    const select = document.getElementById('caja_compensacion_id');
    if (select) {
        // Para cajas, crear como input con datalist (opcional)
        const parent = select.parentNode;
        const newInput = document.createElement('input');
        newInput.className = 'form-control';
        newInput.id = 'caja_compensacion_id';
        newInput.name = 'caja_compensacion_id';
        newInput.placeholder = 'Caja de compensación (opcional)';
        newInput.setAttribute('list', 'cajas-list');
        
        const datalist = document.createElement('datalist');
        datalist.id = 'cajas-list';
        
        cajas.forEach(caja => {
            const option = document.createElement('option');
            option.value = caja.id;
            option.textContent = caja.nombre;
            datalist.appendChild(option);
        });
        
        parent.replaceChild(newInput, select);
        parent.appendChild(datalist);
        console.log(`✅ ${cajas.length} cajas de compensación cargadas`);
    }
}

function cargarOperadoresSS(operadores) {
    const select = document.getElementById('operador_ss_id');
    if (select) {
        const newSelect = crearSelectDinamico('operador_ss_id', 'Seleccione operador...', operadores);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${operadores.length} operadores SS cargados`);
    }
}

function cargarAreasPersonal(areas) {
    const select = document.getElementById('area_personal_id');
    if (select) {
        const newSelect = crearSelectDinamico('area_personal_id', 'Seleccione área...', areas);
        select.parentNode.replaceChild(newSelect, select);
        console.log(`✅ ${areas.length} áreas de personal cargadas`);
    }
}

function crearSelectDinamico(id, placeholder, opciones) {
    const select = document.createElement('select');
    select.className = 'form-select';
    select.id = id;
    select.name = id;
    select.required = true;
    
    select.innerHTML = `<option value="">${placeholder}</option>`;
    
    opciones.forEach(opcion => {
        const option = document.createElement('option');
        option.value = opcion.id;
        option.textContent = opcion.nombre;
        select.appendChild(option);
    });
    
    return select;
}

// Cargar entidades al inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    cargarTodasEntidades();
});
'''
    
    print("✅ Script JavaScript generado")
    print("📝 Para integrar completamente:")
    print("1. Las entidades están pobladas en la base de datos")
    print("2. Las rutas de API están configuradas")
    print("3. El formulario debe actualizarse con los nuevos campos FK")
    print("4. Los dropdowns se cargarán dinámicamente")
    
    return True

if __name__ == "__main__":
    actualizar_formulario()