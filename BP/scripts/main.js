import { system, world, EntityComponentTypes } from '@minecraft/server';
const BROOM = 'witchbroom:broom';
const LANDING_TAG = 'witchbroom:soft_landing';
const EFFECT = 'slow_falling';
const EFFECT_TICKS = 60;
const riders = new Map();
let lastWarning = -1200;
function warn(error) {
    // At most one diagnostic per minute; one removed entity never stops other riders.
    if (system.currentTick - lastWarning >= 1200) {
        console.warn(`[Moonweave Broom] ${String(error)}`);
        lastWarning = system.currentTick;
    }
}
function protect(player) {
    const effect = player.getEffect(EFFECT);
    // Preserve stronger, longer, and infinite (-1) effects from potions/other packs.
    if (!effect || (effect.duration >= 0 && effect.duration < 30 && effect.amplifier === 0)) {
        player.addEffect(EFFECT, EFFECT_TICKS, { amplifier: 0, showParticles: false });
    }
}
function step(player, tick) {
    if (!player.isValid)
        return;
    const mount = player.getComponent(EntityComponentTypes.Riding)?.entityRidingOn;
    const mounted = mount?.typeId === BROOM;
    const guarded = player.hasTag(LANDING_TAG);
    if (!mounted && !guarded) {
        riders.delete(player.id);
        return;
    }
    let state = riders.get(player.id);
    if (!state) {
        state = { mounted: false, graceUntil: tick + 20, groundSamples: 0 };
        riders.set(player.id, state);
        protect(player);
    }
    if (mounted) {
        if (!guarded)
            player.addTag(LANDING_TAG);
        if (!state.mounted) {
            player.onScreenDisplay.setActionBar({ translate: 'witchbroom.controls' });
            protect(player);
        }
        state.mounted = true;
        state.graceUntil = tick + 20;
        state.groundSamples = 0;
        protect(player);
        // Cosmetics only: four tiny bursts/second, only near an occupied broom.
        if (tick % 5 === 0 && mount?.isValid) {
            try {
                const p = mount.location;
                const yaw = mount.getRotation().y * Math.PI / 180;
                mount.dimension.spawnParticle('witchbroom:spark', {
                    x: p.x + Math.sin(yaw) * 0.85,
                    y: p.y + 0.6,
                    z: p.z - Math.cos(yaw) * 0.85,
                });
            }
            catch (error) {
                warn(error);
            }
        }
        return;
    }
    if (state.mounted) {
        state.mounted = false;
        state.graceUntil = tick + 20;
        player.onScreenDisplay.setActionBar({ translate: 'witchbroom.landing' });
    }
    // Never time out a descent: high-altitude protection persists until a real landing.
    // A grace period avoids stale isOnGround values immediately after mounting/reload.
    const safeSurface = player.isOnGround || player.isSwimming;
    state.groundSamples = safeSurface && tick >= state.graceUntil ? state.groundSamples + 1 : 0;
    if (state.groundSamples >= 5) {
        player.removeTag(LANDING_TAG);
        riders.delete(player.id);
        // Do not remove a potion effect. Our last short effect simply expires.
    }
    else {
        protect(player);
    }
}
// One bounded loop; no per-rider timers, world-wide entity scans, or movement teleports.
system.runInterval(() => {
    const tick = system.currentTick;
    const connected = new Set();
    for (const player of world.getAllPlayers()) {
        connected.add(player.id);
        try {
            step(player, tick);
        }
        catch (error) {
            warn(error);
        }
    }
    for (const id of riders.keys())
        if (!connected.has(id))
            riders.delete(id);
}, 1);
world.afterEvents.playerSpawn.subscribe(({ player, initialSpawn }) => {
    // Respawn starts a new life. Rejoining/reloading in mid-air retains the landing tag.
    if (!initialSpawn) {
        try {
            player.removeTag(LANDING_TAG);
        }
        catch (error) {
            warn(error);
        }
        riders.delete(player.id);
    }
});
