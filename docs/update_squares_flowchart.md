# `update_squares()` Flowchart

This diagram shows the execution order inside `update_squares(squares, dt)`.

```mermaid
flowchart TD
    A([Start]) --> B[Create dead_indices list]
    B --> C{For each square in squares}

    C --> D[Find closest small square]
    D --> E{Found a smaller square?}
    E -- Yes --> F[Compute chase vector]
    F --> G[Add chase force to vx and vy]
    E -- No --> H[Skip chase]
    G --> I[Find closest big square]
    H --> I

    I --> J{Found a bigger square?}
    J -- Yes --> K[Compute flee vector]
    K --> L[Add flee force to vx and vy]
    L --> M[Clamp speed to max_speed]
    J -- No --> N[Skip flee]
    M --> O[Advance jitter timer]
    N --> O

    O --> P{Jitter interval reached?}
    P -- Yes --> Q[Reset jitter timer]
    Q --> R[Add random jitter to vx and vy]
    R --> S[Clamp speed to max_speed]
    P -- No --> T[Skip jitter]
    S --> U[Move square by vx * dt and vy * dt]
    T --> U

    U --> V{Hits left/right wall?}
    V -- Yes --> W[Snap x to edge and reverse vx]
    V -- No --> X[Continue]
    W --> Y{Hits top/bottom wall?}
    X --> Y
    Y -- Yes --> Z[Snap y to edge and reverse vy]
    Y -- No --> AA[Continue]

    Z --> AB[Increase age by dt]
    AA --> AB
    AB --> AC{Age >= life_span?}
    AC -- Yes --> AD[Store index in dead_indices]
    AC -- No --> AE[Leave square alive]
    AD --> C
    AE --> C

    C --> AF[Finished iterating squares]
    AF --> AG[Loop through dead_indices in reverse]
    AG --> AH[Remove dead square and append a new one]
    AH --> AI([End])
```

## Order Summary

1. Chase behavior runs first.
2. Flee behavior runs second.
3. Jitter is applied third, only on its timer.
4. Position update happens after all velocity changes.
5. Wall bounce happens after movement.
6. Age/life-span checks happen last.
7. Dead squares are replaced after the main loop finishes.