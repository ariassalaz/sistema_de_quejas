# Opciones para el campo "tipo" de Queja
TIPO_QUEJA = 'queja'
TIPO_SUGERENCIA = 'sugerencia'

OPCIONES_TIPO = [
    (TIPO_QUEJA, 'Queja'),
    (TIPO_SUGERENCIA, 'Sugerencia'),
]

# Opciones para el campo "estado" de Queja
ESTADO_PENDIENTE = 'pendiente'
ESTADO_EN_REVISION = 'en_revision'
ESTADO_RESUELTA = 'resuelta'
ESTADO_RECHAZADA = 'rechazada'

OPCIONES_ESTADO = [
    (ESTADO_PENDIENTE, 'Pendiente'),
    (ESTADO_EN_REVISION, 'En revisión'),
    (ESTADO_RESUELTA, 'Resuelta'),
    (ESTADO_RECHAZADA, 'Rechazada'),
]

# Colores Bootstrap para cada estado
COLOR_ESTADO = {
    ESTADO_PENDIENTE: 'warning',
    ESTADO_EN_REVISION: 'info',
    ESTADO_RESUELTA: 'success',
    ESTADO_RECHAZADA: 'danger',
}
