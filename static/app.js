// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8000';

// Función principal de Alpine.js
function musicApp() {
    return {
        // Estado de la aplicación
        activeTab: 'dashboard',
        loading: false,

        // Datos
        usuarios: [],
        canciones: [],
        favoritos: [],
        stats: {
            usuarios: 0,
            canciones: 0,
            favoritos: 0
        },

        // Modales
        showUserModal: false,
        showSongModal: false,

        // Formularios
        newUser: {
            nombre: '',
            correo: ''
        },
        newSong: {
            titulo: '',
            artista: '',
            album: '',
            duracion: '',
            año: new Date().getFullYear(),
            genero: ''
        },

        // Toast notifications
        toast: {
            show: false,
            message: '',
            type: 'success'
        },

        // Inicialización
        async init() {
            await this.loadAllData();
        },

        // Cargar todos los datos
        async loadAllData() {
            this.loading = true;
            try {
                await Promise.all([
                    this.loadUsuarios(),
                    this.loadCanciones(),
                    this.loadFavoritos()
                ]);
                this.updateStats();
            } catch (error) {
                this.showToast('Error al cargar datos', 'error');
                console.error('Error loading data:', error);
            } finally {
                this.loading = false;
            }
        },

        // Cargar usuarios
        async loadUsuarios() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/usuarios?limit=100`);
                if (!response.ok) throw new Error('Error al cargar usuarios');
                this.usuarios = await response.json();
            } catch (error) {
                console.error('Error loading usuarios:', error);
                throw error;
            }
        },

        // Cargar canciones
        async loadCanciones() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/canciones?limit=100`);
                if (!response.ok) throw new Error('Error al cargar canciones');
                this.canciones = await response.json();
            } catch (error) {
                console.error('Error loading canciones:', error);
                throw error;
            }
        },

        // Cargar favoritos
        async loadFavoritos() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/favoritos?limit=100`);
                if (!response.ok) throw new Error('Error al cargar favoritos');
                this.favoritos = await response.json();
            } catch (error) {
                console.error('Error loading favoritos:', error);
                throw error;
            }
        },

        // Actualizar estadísticas
        updateStats() {
            this.stats = {
                usuarios: this.usuarios.length,
                canciones: this.canciones.length,
                favoritos: this.favoritos.length
            };
        },

        // Crear usuario
        async createUser() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/usuarios`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.newUser)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Error al crear usuario');
                }

                const nuevoUsuario = await response.json();
                this.usuarios.push(nuevoUsuario);
                this.updateStats();

                // Limpiar formulario y cerrar modal
                this.newUser = { nombre: '', correo: '' };
                this.showUserModal = false;

                this.showToast('Usuario creado exitosamente', 'success');
            } catch (error) {
                this.showToast(error.message, 'error');
                console.error('Error creating user:', error);
            }
        },

        // Crear canción
        async createSong() {
            try {
                // Convertir duracion y año a números
                const songData = {
                    ...this.newSong,
                    duracion: parseInt(this.newSong.duracion),
                    año: parseInt(this.newSong.año)
                };

                const response = await fetch(`${API_BASE_URL}/api/canciones`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(songData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Error al crear canción');
                }

                const nuevaCancion = await response.json();
                this.canciones.push(nuevaCancion);
                this.updateStats();

                // Limpiar formulario y cerrar modal
                this.newSong = {
                    titulo: '',
                    artista: '',
                    album: '',
                    duracion: '',
                    año: new Date().getFullYear(),
                    genero: ''
                };
                this.showSongModal = false;

                this.showToast('Canción creada exitosamente', 'success');
            } catch (error) {
                this.showToast(error.message, 'error');
                console.error('Error creating song:', error);
            }
        },

        // Eliminar usuario
        async deleteUser(id) {
            if (!confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/usuarios/${id}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Error al eliminar usuario');
                }

                this.usuarios = this.usuarios.filter(u => u.id !== id);
                // También eliminar favoritos relacionados
                this.favoritos = this.favoritos.filter(f => f.id_usuario !== id);
                this.updateStats();

                this.showToast('Usuario eliminado exitosamente', 'success');
            } catch (error) {
                this.showToast('Error al eliminar usuario', 'error');
                console.error('Error deleting user:', error);
            }
        },

        // Eliminar canción
        async deleteSong(id) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta canción?')) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/canciones/${id}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Error al eliminar canción');
                }

                this.canciones = this.canciones.filter(c => c.id !== id);
                // También eliminar favoritos relacionados
                this.favoritos = this.favoritos.filter(f => f.id_cancion !== id);
                this.updateStats();

                this.showToast('Canción eliminada exitosamente', 'success');
            } catch (error) {
                this.showToast('Error al eliminar canción', 'error');
                console.error('Error deleting song:', error);
            }
        },

        // Eliminar favorito
        async deleteFavorite(id) {
            if (!confirm('¿Estás seguro de que quieres eliminar este favorito?')) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/favoritos/${id}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Error al eliminar favorito');
                }

                this.favoritos = this.favoritos.filter(f => f.id !== id);
                this.updateStats();

                this.showToast('Favorito eliminado exitosamente', 'success');
            } catch (error) {
                this.showToast('Error al eliminar favorito', 'error');
                console.error('Error deleting favorite:', error);
            }
        },

        // Ver favoritos de un usuario
        viewUserFavorites(userId) {
            const userFavorites = this.favoritos.filter(f => f.id_usuario === userId);
            const userName = this.getUserName(userId);

            if (userFavorites.length === 0) {
                this.showToast(`${userName} no tiene favoritos`, 'error');
                return;
            }

            // Cambiar a la pestaña de favoritos
            this.activeTab = 'favoritos';
            this.showToast(`Mostrando favoritos de ${userName}`, 'success');
        },

        // Obtener nombre de usuario por ID
        getUserName(userId) {
            const user = this.usuarios.find(u => u.id === userId);
            return user ? user.nombre : 'Usuario desconocido';
        },

        // Obtener título de canción por ID
        getSongTitle(songId) {
            const song = this.canciones.find(c => c.id === songId);
            return song ? `${song.titulo} - ${song.artista}` : 'Canción desconocida';
        },

        // Mostrar toast notification
        showToast(message, type = 'success') {
            this.toast = {
                show: true,
                message,
                type
            };

            // Auto-hide después de 3 segundos
            setTimeout(() => {
                this.toast.show = false;
            }, 3000);
        },

        // Formatear duración de canción
        formatDuration(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
        },

        // Formatear fecha
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        },

        // Buscar en datos
        searchData(query, type) {
            if (!query) return;

            query = query.toLowerCase();

            switch (type) {
                case 'usuarios':
                    return this.usuarios.filter(u =>
                        u.nombre.toLowerCase().includes(query) ||
                        u.correo.toLowerCase().includes(query)
                    );
                case 'canciones':
                    return this.canciones.filter(c =>
                        c.titulo.toLowerCase().includes(query) ||
                        c.artista.toLowerCase().includes(query) ||
                        c.album.toLowerCase().includes(query) ||
                        c.genero.toLowerCase().includes(query)
                    );
                default:
                    return [];
            }
        }
    };
}

// Funciones de utilidad globales
window.musicUtils = {
    // Validar email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Validar año
    isValidYear(year) {
        const currentYear = new Date().getFullYear();
        return year >= 1900 && year <= currentYear + 10;
    },

    // Capitalizar primera letra
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },

    // Generar color aleatorio para avatares
    getRandomColor() {
        const colors = [
            '#1DB954', '#FF6B35', '#F7931E', '#FFD23F',
            '#06FFA5', '#4ECDC4', '#45B7D1', '#96CEB4',
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
};

// Interceptor para manejo de errores de red
window.addEventListener('unhandledrejection', event => {
    console.error('Unhandled promise rejection:', event.reason);

    // Mostrar mensaje de error genérico si la API no está disponible
    if (event.reason && event.reason.message && event.reason.message.includes('fetch')) {
        const app = Alpine.store('app');
        if (app && app.showToast) {
            app.showToast('Error de conexión con la API. Verifica que el servidor esté ejecutándose.', 'error');
        }
    }
});

// Log para debugging
console.log('🎵 Music App JavaScript loaded successfully!');
console.log('📡 API Base URL:', API_BASE_URL);
