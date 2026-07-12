# System Architecture Overview

## Purpose
This document explains how this system is structured and why.

## Architectural Style
- Domain-Driven Design (DDD)
- Clean Architecture
- Hexagonal Architecture
- Event-Driven where scale requires

## Core Principles
- Business logic is isolated
- Dependencies point inward
- Domains are autonomous
- Contracts over shared code
- Observability is mandatory

## Folder Overview
- core/domains → Business capabilities
- core/shared_kernel → Stable primitives
- core/platform → Infrastructure tooling
- core/observability → Logs, traces, metrics
- core/governance → Architecture enforcement

## Team Ownership
Each domain is owned by one autonomous team.
Teams build and run what they own.

## Change Process
- Small change → normal PR
- Large change → Architecture Review + ADR

## Longevity Goal
This architecture is designed to:
- Support 100+ developers
- Survive technology changes
- Scale for decades
