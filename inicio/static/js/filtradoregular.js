document.addEventListener('DOMContentLoaded', function() {
    // Referencias a los elementos
    const tipoPrograma = document.getElementById('tipoPrograma');
    const tipoModalidad = document.getElementById('tipoModalidad');
    const nombrePrograma = document.getElementById('nombrePrograma');
    const horasPrograma = document.getElementById('horasPrograma');
    const codigoCurso = document.getElementById('codigoCurso');
    const versionPrograma = document.getElementById('versionPrograma');
    const departamentoFormacion = document.getElementById('departamentoFormacion');
    const municipioFormacion = document.getElementById('municipioFormacion');
    const tieneEmpresa = document.getElementById('tieneEmpresa');
    
    // Referencias a campos de empresa
    const empresaSolicitante = document.getElementById('empresaSolicitante');
    const tipoEmpresa = document.getElementById('tipoEmpresa');
    const nombreResponsable = document.getElementById('nombreResponsable');
    const correoResponsable = document.getElementById('correoResponsable');
    const nitEmpresa = document.getElementById('nitEmpresa');
    const cartaSolicitud = document.getElementById('cartaSolicitud');

    // Función para mostrar/ocultar campos de empresa
    function toggleCamposEmpresa() {
        if (!tieneEmpresa) return;
        
        const mostrar = tieneEmpresa.value === 'si';
        
        // Lista de elementos de empresa
        const elementosEmpresa = [
            empresaSolicitante,
            tipoEmpresa, 
            nombreResponsable,
            correoResponsable,
            nitEmpresa,
            cartaSolicitud
        ];
        
        elementosEmpresa.forEach(function(elemento) {
            if (elemento) {
                const contenedor = elemento.closest('.campo-entrada');
                if (contenedor) {
                    contenedor.style.display = mostrar ? 'block' : 'none';
                }
                
                // Manejar atributo required
                if (mostrar) {
                    elemento.setAttribute('required', 'required');
                } else {
                    elemento.removeAttribute('required');
                    elemento.value = ''; // Limpiar valor cuando se oculta
                }
            }
        });
    }

    // Función para filtrar programas por tipo y modalidad
    function filtrarProgramas() {
        if (!tipoPrograma || !tipoModalidad || !nombrePrograma) return;
        
        const tipoSeleccionado = tipoPrograma.value;
        const modalidadSeleccionada = tipoModalidad.value;
        const horasSeleccionadas = horasPrograma ? horasPrograma.value : '';
        
        const opciones = nombrePrograma.querySelectorAll('option');
        
        // Limpiar selección actual
        nombrePrograma.value = '';
        limpiarCamposReadonly();
        
        opciones.forEach(function(opcion) {
            if (opcion.value === '') {
                opcion.style.display = 'block';
                return;
            }
            
            const areaPrograma = opcion.getAttribute('data-area');
            const modalidadPrograma = opcion.getAttribute('data-modalidad');
            const horasProg = opcion.getAttribute('data-horas');
            
            if ((!tipoSeleccionado || areaPrograma === tipoSeleccionado) &&
                (!modalidadSeleccionada || modalidadPrograma === modalidadSeleccionada) &&
                (!horasSeleccionadas || horasProg === horasSeleccionadas)) {
                opcion.style.display = 'block';
            } else {
                opcion.style.display = 'none';
            }
        });
        // Si después de filtrar solo hay una opción visible (además del placeholder), seleccionarla automáticamente
        const visibles = Array.from(opciones).filter(o => o.value !== '' && o.style.display !== 'none');
        if (visibles.length === 1) {
            visibles[0].selected = true;
            llenarCamposReadonly();
        }
    }

    // Función para llenar campos readonly
    function llenarCamposReadonly() {
        if (!nombrePrograma) return;
        
        const opcionSeleccionada = nombrePrograma.selectedOptions[0];
        if (opcionSeleccionada && opcionSeleccionada.value !== '') {
            const horas = opcionSeleccionada.getAttribute('data-horas');
            const version = opcionSeleccionada.getAttribute('data-version');
            const codigo = opcionSeleccionada.value;
            
            if (versionPrograma) versionPrograma.value = version || '';
            if (codigoCurso) codigoCurso.value = codigo || '';
        }
    }

    // Construir dinámicamente las opciones del select de horas según los programas disponibles
    function construirSelectHoras() {
        if (!horasPrograma || !nombrePrograma) return;
        const opciones = nombrePrograma.querySelectorAll('option[data-horas]');
        const setHoras = new Set();
        opciones.forEach(o => {
            const h = o.getAttribute('data-horas');
            if (h) setHoras.add(h);
        });
        // Guardar selección previa
        const previa = horasPrograma.value;
        // Limpiar (dejando primera opción)
        horasPrograma.innerHTML = '<option value="">Todas las horas</option>';
        Array.from(setHoras).sort((a,b)=>parseInt(a)-parseInt(b)).forEach(h => {
            const opt = document.createElement('option');
            opt.value = h;
            opt.textContent = h + ' horas';
            horasPrograma.appendChild(opt);
        });
        // Restaurar si aún existe
        if (previa && setHoras.has(previa)) {
            horasPrograma.value = previa;
        }
    }

    // Función para limpiar campos readonly
    function limpiarCamposReadonly() {
        if (versionPrograma) versionPrograma.value = '';
        if (codigoCurso) codigoCurso.value = '';
    }

    // Función para filtrar municipios por departamento
    function filtrarMunicipios() {
        if (!departamentoFormacion || !municipioFormacion) return;
        
        const departamentoSeleccionado = departamentoFormacion.value;
        const opciones = municipioFormacion.querySelectorAll('option');
        
        // Limpiar selección actual
        municipioFormacion.value = '';
        
        opciones.forEach(function(opcion) {
            if (opcion.value === '') {
                opcion.style.display = 'block';
                return;
            }
            
            const departamentoMunicipio = opcion.getAttribute('data-departamento');
            
            if (!departamentoSeleccionado || departamentoMunicipio === departamentoSeleccionado) {
                opcion.style.display = 'block';
            } else {
                opcion.style.display = 'none';
            }
        });
    }

    // Event listeners con verificación
    if (tipoPrograma) tipoPrograma.addEventListener('change', filtrarProgramas);
    if (tipoModalidad) tipoModalidad.addEventListener('change', filtrarProgramas);
    if (horasPrograma) horasPrograma.addEventListener('change', filtrarProgramas);
    if (nombrePrograma) nombrePrograma.addEventListener('change', llenarCamposReadonly);
    if (departamentoFormacion) departamentoFormacion.addEventListener('change', filtrarMunicipios);
    if (tieneEmpresa) tieneEmpresa.addEventListener('change', toggleCamposEmpresa);
    
    // Validación del formulario
    const formulario = document.querySelector('.formulario-ficha');
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            let isValid = true;
            let mensajeError = '';
            
            // Validar que al menos un día de la semana esté seleccionado
            const diasSeleccionados = document.querySelectorAll('input[name="diasSemana[]"]:checked');
            if (diasSeleccionados.length === 0) {
                mensajeError += 'Debe seleccionar al menos un día de la semana.\n';
                isValid = false;
            }
            
            // Validar campos de empresa si está seleccionado "Sí"
            if (tieneEmpresa && tieneEmpresa.value === 'si') {
                const camposEmpresaRequeridos = [
                    {elemento: empresaSolicitante, nombre: 'Empresa Solicitante'},
                    {elemento: tipoEmpresa, nombre: 'Tipo de Empresa'},
                    {elemento: nombreResponsable, nombre: 'Nombre del Responsable'},
                    {elemento: correoResponsable, nombre: 'Correo Electrónico'},
                    {elemento: nitEmpresa, nombre: 'NIT de la Empresa'},
                    {elemento: cartaSolicitud, nombre: 'Carta de Solicitud'}
                ];
                
                camposEmpresaRequeridos.forEach(function(campo) {
                    if (campo.elemento && !campo.elemento.value.trim()) {
                        mensajeError += `El campo "${campo.nombre}" es requerido cuando hay empresa.\n`;
                        isValid = false;
                    }
                });
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('Por favor corrija los siguientes errores:\n\n' + mensajeError);
            }
        });
    }
    
    // Configuración inicial
    construirSelectHoras();
    filtrarProgramas();
    filtrarMunicipios();
    toggleCamposEmpresa(); // Ocultar campos de empresa inicialmente
});