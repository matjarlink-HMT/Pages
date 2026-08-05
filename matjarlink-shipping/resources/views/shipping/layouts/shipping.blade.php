{{--
    غلاف الوحدة. يمتد قالب المنصة الرئيسي (layouts.app) فيرث الهيدر
    والتنقل والهوية البصرية كاملة — المستخدم يشعر أنها جزء أصيل من متجرلينك
    لا نظام منفصل. عدّل اسم القالب الموروث ليطابق ما هو قائم في المنصة.
--}}
@extends('layouts.app')

@section('title', $title ?? __('shipping.module'))

@push('styles')
    <link rel="stylesheet" href="{{ asset('css/shipping.css') }}">
@endpush

@section('content')
    <div class="ship" dir="{{ app()->getLocale() === 'ar' ? 'rtl' : 'ltr' }}">

        <nav class="ship-tabs" aria-label="{{ __('shipping.module') }}">
            <a href="{{ route('shipping.dashboard') }}"
               class="ship-tab @if(request()->routeIs('shipping.dashboard')) is-active @endif">
                {{ __('shipping.dashboard') }}
            </a>
            <a href="{{ route('shipping.shipments.index') }}"
               class="ship-tab @if(request()->routeIs('shipping.shipments.index')) is-active @endif">
                {{ __('shipping.shipments') }}
            </a>
            <a href="{{ route('shipping.shipments.create') }}"
               class="ship-tab @if(request()->routeIs('shipping.shipments.create')) is-active @endif">
                {{ __('shipping.create_shipment') }}
            </a>
            <a href="{{ route('shipping.carrier-accounts.index') }}"
               class="ship-tab @if(request()->routeIs('shipping.carrier-accounts.*')) is-active @endif">
                {{ __('shipping.carriers') }}
            </a>
        </nav>

        @if (session('status'))
            <div class="ship-alert ship-alert--ok" role="status">{{ session('status') }}</div>
        @endif

        @if ($errors->any())
            <div class="ship-alert ship-alert--danger" role="alert">
                <ul class="ship-list">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        @yield('shipping')
    </div>
@endsection
