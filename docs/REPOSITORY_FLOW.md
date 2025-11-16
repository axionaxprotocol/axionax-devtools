# axionax Repository Connection Flow

## Connection Diagram

```mermaid
graph TD
    axionax_core["✅ axionax-core"]
    axionax_web["✅ axionax-web"]
    axionax_sdk_ts["✅ axionax-sdk-ts"]
    axionax_marketplace["✅ axionax-marketplace"]
    axionax_docs["✅ axionax-docs"]
    axionax_deploy["✅ axionax-deploy"]
    axionax_devtools["✅ axionax-devtools"]
    axionax_core -->|docs:reference(4)| axionax_web
    axionax_core -->|docs:reference(9)| axionax_sdk_ts
    axionax_core -->|docs:reference(4)| axionax_marketplace
    axionax_core -->|docs:reference(6)| axionax_docs
    axionax_core -->|docs:reference(4)| axionax_deploy
    axionax_core -->|docs:reference(4)| axionax_devtools
    axionax_web -->|docs:reference(7)| axionax_core
    axionax_web -->|docs:reference(7)| axionax_sdk_ts
    axionax_web -->|docs:reference(4)| axionax_marketplace
    axionax_web -->|docs:reference(7)| axionax_docs
    axionax_web -->|docs:reference(8)| axionax_deploy
    axionax_web -->|docs:reference(4)| axionax_devtools
    axionax_sdk_ts -->|docs:reference(4)| axionax_core
    axionax_sdk_ts -->|docs:reference(1)| axionax_web
    axionax_sdk_ts -->|docs:reference(1)| axionax_marketplace
    axionax_marketplace -->|docs:reference(4)| axionax_core
    axionax_marketplace -->|docs:reference(2)| axionax_docs
    axionax_docs -->|docs:reference(11)| axionax_core
    axionax_docs -->|docs:reference(5)| axionax_web
    axionax_docs -->|docs:reference(4)| axionax_sdk_ts
    axionax_docs -->|docs:reference(4)| axionax_marketplace
    axionax_docs -->|docs:reference(5)| axionax_deploy
    axionax_docs -->|docs:reference(4)| axionax_devtools
    axionax_deploy -->|docs:reference(8)| axionax_core
    axionax_deploy -->|docs:reference(5)| axionax_web
    axionax_deploy -->|docs:reference(3)| axionax_sdk_ts
    axionax_deploy -->|docs:reference(2)| axionax_marketplace
    axionax_deploy -->|docs:reference(5)| axionax_docs
    axionax_deploy -->|docs:reference(2)| axionax_devtools
    axionax_devtools -->|docs:reference(4)| axionax_core
    axionax_devtools -->|docs:reference(4)| axionax_web
    axionax_devtools -->|docs:reference(4)| axionax_sdk_ts
    axionax_devtools -->|docs:reference(2)| axionax_marketplace
    axionax_devtools -->|docs:reference(2)| axionax_docs
    axionax_devtools -->|docs:reference(2)| axionax_deploy

    classDef coreStyle fill:#ff6b6b,stroke:#c92a2a,stroke-width:2px
    classDef webStyle fill:#4ecdc4,stroke:#219a91,stroke-width:2px
    classDef toolStyle fill:#ffe66d,stroke:#cca300,stroke-width:2px
    classDef sdkStyle fill:#a8e6cf,stroke:#64b58b,stroke-width:2px

    class axionax_core coreStyle
    class axionax_web,axionax_marketplace webStyle
    class axionax_devtools,axionax_deploy toolStyle
    class axionax_sdk_ts,axionax_docs sdkStyle
```

## Legend

- 🔴 **Core**: axionax-core (main protocol implementation)
- 🔵 **Web**: axionax-web, axionax-marketplace (web interfaces)
- 🟡 **Tools**: axionax-devtools, axionax-deploy (development & deployment)
- 🟢 **SDK/Docs**: axionax-sdk-ts, axionax-docs (libraries & documentation)
