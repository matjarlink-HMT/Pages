# ٠٦ — هيكل المشروع

## ١. الشجرة الكاملة

```
app/Domains/Shipping/
│
├── ShippingServiceProvider.php          # تسجيل الـ Drivers، الأحداث، السياسات، المسارات
├── ShippingFacade.php                   # الواجهة الوحيدة المسموح استدعاؤها من خارج الوحدة
│
├── Models/
│   ├── Shipment.php                     # + TenantScope, HasStates, LogsActivity
│   ├── ShipmentAddress.php
│   ├── ShipmentPackage.php
│   ├── ShipmentItem.php
│   ├── ShipmentEvent.php
│   ├── ShipmentLabel.php
│   ├── ShipmentNotification.php
│   ├── ShipmentReturn.php
│   ├── ShipmentClaim.php
│   ├── ShippingCarrier.php
│   ├── StoreCarrierAccount.php          # credentials => 'encrypted:json'
│   ├── CarrierStatusMap.php
│   ├── ShippingZone.php / ShippingZoneRegion.php
│   ├── ShippingRateCard.php / ShippingRateRule.php
│   ├── RateQuote.php
│   ├── PickupRequest.php
│   ├── CodSettlement.php
│   ├── CarrierWebhookEvent.php / CarrierApiLog.php
│   ├── ShippingSettings.php
│   ├── ShippingAutomationRule.php
│   ├── ShippingAddressBook.php
│   └── CarrierPerformanceDaily.php
│
├── Enums/
│   ├── ShipmentStatus.php               # + label(), color(), isTerminal(), icon()
│   ├── ShipmentEventSource.php
│   ├── PaymentType.php
│   ├── LabelFormat.php
│   ├── NotificationChannel.php
│   ├── ClaimType.php / ClaimStatus.php
│   └── ReturnStatus.php
│
├── StateMachine/
│   ├── ShipmentStateMachine.php         # قواعد الانتقال المسموحة
│   └── Transitions/                     # منطق خاص لكل انتقال عند الحاجة
│
├── DTOs/
│   ├── RateRequest.php / RateQuoteData.php / RateQuoteCollection.php
│   ├── ShipmentRequest.php / CarrierShipmentResult.php
│   ├── TrackingEventData.php / TrackingEventCollection.php
│   ├── AddressData.php / PackageData.php
│   ├── CarrierCapabilities.php / ConnectionResult.php
│   ├── PickupRequestData.php / PickupResult.php
│   ├── LabelFile.php / CancellationResult.php
│   └── WebhookPayload.php
│
├── Services/
│   ├── ShipmentCreationService.php
│   ├── BulkShipmentService.php
│   ├── RateComparisonService.php
│   ├── RateCardEngine.php
│   ├── CoverageResolver.php
│   ├── LabelService.php
│   ├── TrackingSyncService.php
│   ├── WebhookIngestionService.php
│   ├── StatusNormalizer.php
│   ├── ShipmentEventRecorder.php
│   ├── ShipmentNotificationService.php
│   ├── ShippingAnalyticsService.php
│   ├── CodReconciliationService.php
│   ├── CarrierInvoiceAuditService.php
│   ├── SlaEngine.php
│   ├── AutomationRuleEngine.php
│   ├── CarrierHealthCheckService.php
│   ├── PublicTrackingService.php
│   └── AddressBookService.php
│
├── Actions/                             # حالة استخدام واحدة لكل ملف
│   ├── CreateShipmentAction.php
│   ├── CancelShipmentAction.php
│   ├── RegenerateLabelAction.php
│   ├── RecordManualEventAction.php
│   ├── ConnectCarrierAccountAction.php
│   ├── TestCarrierConnectionAction.php
│   ├── SchedulePickupAction.php
│   ├── OpenClaimAction.php
│   └── CreateReturnShipmentAction.php
│
├── Integration/
│   ├── CarrierRegistry.php
│   ├── Contracts/
│   │   ├── CarrierDriver.php
│   │   ├── SupportsPickup.php           # واجهات اختيارية بدل تضخيم العقد
│   │   ├── SupportsReturns.php
│   │   └── SupportsWebhooks.php
│   ├── Concerns/
│   │   ├── MakesHttpRequests.php        # مهلات + إعادة محاولة + تسجيل + معرّف ارتباط
│   │   ├── HandlesCircuitBreaker.php
│   │   └── LogsCarrierCalls.php
│   ├── Drivers/
│   │   ├── AbstractCarrierDriver.php
│   │   ├── Manual/ManualDriver.php      # الشركات بلا API
│   │   ├── Asyad/  { AsyadDriver, AsyadMapper, AsyadWebhookVerifier, config.php }
│   │   ├── OmanPost/…
│   │   ├── Aramex/…
│   │   ├── Smsa/…
│   │   ├── Dhl/…
│   │   ├── Imile/…
│   │   └── Naqel/…
│   └── Exceptions/
│       ├── CarrierException.php
│       ├── CarrierUnavailableException.php
│       ├── DestinationNotCoveredException.php
│       └── InvalidCredentialsException.php
│
├── Events/          … ShipmentCreated, ShipmentStatusChanged, ShipmentDelivered,
│                      ShipmentDelayed, ShipmentReturned, ShipmentCancelled,
│                      CarrierConnectionFailed, LabelGenerated
├── Listeners/       … UpdateOrderFromShipment, SendShipmentNotification,
│                      RecordShipmentActivity, UpdateCarrierAnalytics,
│                      ReleaseInventoryOnDelivery, OpenClaimOnLoss
│
├── Jobs/            … CreateCarrierShipmentJob, ProcessCarrierWebhookJob,
│                      SyncShipmentTrackingJob, GenerateLabelJob, MergeLabelsPdfJob,
│                      BulkCreateShipmentsJob, RollupCarrierPerformanceJob,
│                      DetectDelayedShipmentsJob, CarrierHealthCheckJob,
│                      ExportShipmentsJob, PruneApiLogsJob
│
├── Notifications/
│   ├── ShipmentCreatedNotification.php
│   ├── ShipmentOutForDeliveryNotification.php
│   ├── ShipmentDeliveredNotification.php
│   ├── ShipmentDelayedNotification.php
│   ├── DeliveryFailedNotification.php
│   └── Channels/ { WhatsAppChannel.php, SmsChannel.php }
│
├── Http/
│   ├── Controllers/
│   │   ├── Merchant/  { DashboardController, ShipmentController, RateController,
│   │   │                CarrierAccountController, ZoneController, RateCardController,
│   │   │                PickupController, ReturnController, ClaimController,
│   │   │                ReportController, SettingsController, AutomationRuleController,
│   │   │                WebhookEventController }
│   │   ├── Webhooks/CarrierWebhookController.php
│   │   ├── Public/PublicTrackingController.php
│   │   └── Partner/PartnerShipmentController.php
│   ├── Requests/     … CreateShipmentRequest, RateRequest, ConnectCarrierRequest, …
│   ├── Resources/    … ShipmentResource, ShipmentDetailResource, RateQuoteResource,
│   │                    CarrierAccountResource, PublicTrackingResource
│   ├── Middleware/   … EnsureShippingEnabled, VerifyCarrierWebhookSignature,
│   │                    ThrottlePublicTracking
│   └── Filters/      … ShipmentFilter (فلترة معلنة وآمنة)
│
├── Policies/         … ShipmentPolicy, CarrierAccountPolicy, ReportPolicy,
│                       ClaimPolicy, SettingsPolicy
│
├── Views/  (resources/views/shipping)
│   ├── layouts/shipping.blade.php
│   ├── dashboard.blade.php
│   ├── shipments/ { index, show, create, bulk }.blade.php
│   ├── carriers/  { index, connect }.blade.php
│   ├── zones/, rate-cards/, pickups/, returns/, claims/, reports/, settings/
│   ├── labels/    { a4, thermal_10x15, packing_slip, pick_list }.blade.php
│   ├── public/track.blade.php
│   └── components/ { status-badge, carrier-logo, timeline, stat-tile,
│                     rate-card-option, shipment-filters, attention-list }
│
├── Livewire/         … ShipmentTable, ShipmentWizard, RateComparison,
│                       CarrierConnectionCard, ShipmentTimeline, BulkShipStation,
│                       DashboardStats, ReportBuilder
│
├── Support/
│   ├── WeightCalculator.php             # الوزن الحجمي والقابل للفوترة
│   ├── ReferenceGenerator.php           # SHP-2026-000123
│   ├── PhoneNormalizer.php              # صيغة +968
│   ├── AddressFormatter.php
│   ├── BarcodeGenerator.php
│   ├── OmanGeo.php                      # المحافظات والولايات
│   └── CredentialMasker.php
│
└── Console/Commands/
    ├── shipping:sync-tracking
    ├── shipping:test-carrier {account}
    ├── shipping:rollup-performance
    ├── shipping:replay-webhook {id}
    └── shipping:seed-carriers
```

## ٢. خارج مجلد الوحدة

```
database/migrations/shipping/          # ٢٤ هجرة مرقّمة
database/seeders/ShippingCarrierSeeder.php
database/seeders/OmanGeoSeeder.php
config/shipping.php                    # المهلات، الأوزان الافتراضية، أوزان التوصية، الطوابير
routes/shipping.php                    # مسارات لوحة التاجر
routes/shipping-webhooks.php
routes/shipping-public.php
lang/ar/shipping.php  +  lang/en/shipping.php
resources/js/shipping/                 # Alpine components (طباعة، مسح باركود، خرائط)
resources/css/shipping.css             # امتداد لنظام تصميم المنصة لا بديل عنه
tests/Feature/Shipping/                # اختبارات المسارات وسير العمل
tests/Unit/Shipping/                   # الخدمات، محرك التسعير، آلة الحالات
tests/Fixtures/Carriers/               # ردود API محفوظة لكل شركة
```

## ٣. قواعد الحدود (Boundaries)

يُفرض بأداة تحليل ثابت (Deptrac أو ما يعادلها) في التكامل المستمر:

1. **لا كود خارج الوحدة يستورد `App\Domains\Shipping\Models\*`** — الوصول عبر `ShippingFacade` أو الأحداث فقط.
2. **الوحدة لا تستورد موديلات الطلبات مباشرة** — عبر `OrderShippingBridge` وواجهة `OrderRepositoryInterface` تُحقن.
3. **طبقة Domain لا تستورد `Integration` ولا `Http`.**
4. **الـ Drivers لا تستورد `Models`** — تتعامل مع DTOs فقط، ما يجعلها قابلة للاختبار بلا قاعدة بيانات.
5. **لا استعلام قاعدة بيانات داخل Blade** — كل البيانات من Livewire/Controller.

## ٤. إضافة شركة شحن جديدة (سير عمل كامل)

```
١. php artisan shipping:make-driver Nool
   → ينشئ Drivers/Nool/{NoolDriver, NoolMapper, config.php} + هيكل اختبار
٢. نفّذ العقد (٦ دوال إلزامية، والبقية من AbstractCarrierDriver)
٣. عرّف statusMap() ← تُبذَر في carrier_status_maps
٤. أضف صفاً في shipping_carriers (Seeder)
٥. اكتب اختبارات مقابل ردود محفوظة في tests/Fixtures/Carriers/nool/
٦. سجّل الـ Driver في ShippingServiceProvider (سطر واحد)
```
**لا تعديل** على: النواة، الواجهات، قاعدة البيانات، التقارير، الإشعارات. هذا هو معيار نجاح المعمارية.
