"""
    Describes the states of the application.

    This is to ensure that the states are according to the database, and any change made is reflected both
    on database and this utility file.
"""
ORDER_CREATING = 'Creating'
ORDER_PLACED = 'Placed'
ORDER_PAID = 'Paid'
ORDER_CANCELLED = 'Cancelled'
ORDER_REQUESTED_REFUND = 'Requested Refund'
ORDER_REFUNDED = 'Refunded'

ORDER_ACTIONS_FORCE_CANCEL = 'Force cancel'
ORDER_ACTIONS_REFUND = 'Refund'
ORDER_ACTIONS_UPDATE_REFERENCE = 'Update Reference'

TRACKINGS_CANCELLED = 'Cancelled'
TRACKINGS_REFUNDED = 'Refunded'

orders_states = {
    'creating': ORDER_CREATING,
    'placed': ORDER_PLACED,
    'paid': ORDER_PLACED,
    'cancelled': ORDER_CANCELLED,
    'requested_refund': ORDER_REQUESTED_REFUND,
    'refunded': ORDER_REFUNDED,
}

orders_actions = {
    'force_cancel': ORDER_ACTIONS_FORCE_CANCEL,
    'refund': ORDER_ACTIONS_REFUND,
}
