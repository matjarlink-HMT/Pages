<?php

declare(strict_types=1);

return [

    'module' => 'Shipping',
    'dashboard' => 'Dashboard',
    'shipments' => 'Shipments',
    'create_shipment' => 'Create shipment',
    'carriers' => 'Carriers',
    'reports' => 'Reports',

    'status' => [
        'draft' => 'Draft',
        'pending_carrier' => 'Pending carrier',
        'carrier_error' => 'Carrier error',
        'created' => 'Created',
        'picked_up' => 'Picked up',
        'in_transit' => 'In transit',
        'out_for_delivery' => 'Out for delivery',
        'delivered' => 'Delivered',
        'failed_attempt' => 'Failed attempt',
        'exception' => 'Exception',
        'returning' => 'Returning',
        'returned' => 'Returned',
        'cancelled' => 'Cancelled',
        'lost' => 'Lost',
        'damaged' => 'Damaged',
    ],

    'source' => [
        'webhook' => 'Webhook',
        'polling' => 'Sync',
        'manual' => 'Manual',
        'system' => 'System',
        'import' => 'Import',
    ],

    'payment' => [
        'prepaid' => 'Prepaid',
        'cod' => 'Cash on delivery',
        'carrier_account' => 'Carrier account',
    ],

    'connection' => [
        'unknown' => 'Not connected',
        'connected' => 'Connected',
        'failed' => 'Connection failed',
    ],

    'features' => [
        'tracking' => 'Live tracking',
        'cod' => 'Cash on delivery',
        'insurance' => 'Insurance',
        'pickup' => 'Pickup',
    ],

    'rates' => [
        'same_day' => 'Same day',
        'days' => '{1} 1 business day|[2,*] :count business days',
        'days_range' => ':min–:max business days',
        'recommended' => 'Best match',
        'cheapest' => 'Cheapest',
        'unavailable_title' => 'Unavailable for this shipment',
    ],

    'unavailable' => [
        'not_covered' => 'Does not cover :area',
        'connection_failed' => 'Could not reach the carrier',
        'no_rate' => 'No rate for this shipment',
        'account_inactive' => 'Account is inactive',
    ],

    'events' => [
        'created' => 'Shipment created and label issued',
        'cancelled' => 'Shipment cancelled',
        'carrier_error' => 'Could not send shipment to the carrier — :reason',
    ],

    'errors' => [
        'shipping_carrier_error' => 'The carrier returned an error. Try again or pick another carrier.',
        'shipping_carrier_unavailable' => 'Carrier is unavailable right now.',
        'shipping_destination_not_covered' => 'The selected carrier does not cover this destination.',
        'shipping_invalid_credentials' => 'Credentials were rejected — check the account settings.',
        'shipping_duplicate_request' => 'This shipment already exists.',
        'no_rate_for_destination' => 'No rate covers this destination.',
        'cancellation_unsupported' => 'This carrier does not support cancellation via API.',
        'already_terminal' => 'Shipment already reached a final state.',
    ],

    'validation' => [
        'unknown_wilayat' => 'The selected wilayat does not belong to this governorate.',
    ],

    'manual' => [
        'ready' => 'Manual delivery is ready — rate card active.',
        'no_rate_card' => 'No active rate card for this account.',
    ],

    'flash' => [
        'created' => 'Shipment :reference created and label issued.',
        'cancelled' => 'Shipment cancelled.',
        'sync_queued' => 'Tracking update requested.',
        'event_recorded' => 'Event recorded.',
        'export_queued' => 'Export is being prepared.',
        'carrier_connected' => 'Carrier connected and activated.',
        'carrier_failed' => 'Account saved but connection failed: :reason',
        'carrier_updated' => 'Account updated.',
        'carrier_removed' => 'Account removed.',
        'connection_ok' => 'Connection successful.',
        'connection_failed' => 'Connection failed: :reason',
        'default_set' => 'Default carrier set.',
    ],

    'attention' => [
        'delayed' => 'Delayed shipments',
        'stale' => 'No update for 72h',
        'failed_attempt' => 'Failed deliveries',
        'carrier_error' => 'Carrier send failures',
    ],

    'ui' => [
        'attention' => 'Needs your attention',
        'delayed' => 'Delayed',
        'stale' => 'No updates',
        'total_shipments' => 'Total shipments',
        'total_cost' => 'Total shipping cost',
        'avg_cost' => 'Average per shipment',
        'avg_delivery' => 'Average delivery time',
        'on_time_rate' => 'On-time delivery',
        'cod_pending' => 'Pending COD',
        'invoice_variance' => 'Invoice variance',
        'top_wilayats' => 'Top wilayats',
        'billable_weight' => 'Billable weight',
        'volumetric_hint' => 'Carriers bill the greater of actual and volumetric weight.',
        'timeline' => 'Timeline',
        'no_shipments' => 'No shipments yet.',
        'no_results' => 'No matching results.',
        'clear_filters' => 'Clear filters',
        'load_more' => 'Load more',
    ],
];
