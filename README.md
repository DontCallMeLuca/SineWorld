# ✨ Sine World
###### _A world made from the sine function_

## What
This is a world generated using sine as the noise function.
Literally everything you see in the scene is made from sine.
<br>

```glsl
float noise(vec2 p) {
    return sin(p[0]) + sin(p[1]);
}
```

This very simple noise function, which uses sine,
is what's used to generate the terrain, water, sky, textures and more.

```glsl
float fbm(vec2 p) {
    float res = 0.0;
    float amp = 0.5;
    float freq = 1.95;
    for( int i = 0; i < NUM_OCTAVES; i++) {
        res += amp * noise(p);
        amp *= 0.5;
        p = p * freq * rot(PI / 4.0) - res * 0.4;
    }
    return res;
}
```

This function is an implementation of **Fractal Brownian Motion (FBM)**
<br>
This is more or less where the generation really takes place.
<br>
It makes use of the noise function generate practically everything.
<br>
You can modify its constants to change the world how you please.

- `res` stores the accumulated noise result.
- `amp` controls the amplitude of the noise.
- `freq` controls the level of detail in the noise. 

Another pro tip, if you want to have only water in the scene:

```glsl
float map(vec3 p) {
    float d = 50.0; // Change from 0.0 to 50.0
    d += getTerrain(p);
    return min(d, getWater(p) + d);
}
```

This simple change will raise the water level above the terrain.

## Showcase

## Why
After experimenting with minecraft word generation via noise functions to create
a world of voxels, I realized every single mathemtical function could become a noise
function, and could be used to generate entire worlds. So I thought, why not use
one of the most basic functions, sine, and see what comes out of it.