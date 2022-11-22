const scene = new THREE.Scene();
// const camera1 = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
const camera1 = new THREE.OrthographicCamera(-48, 48, 27, -27, 1, 1000);
const camera2 = new THREE.OrthographicCamera(-48, 48, 27, -27, 1, 1000);
scene.add(camera2);

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const clock = new THREE.Clock();

const orb_speed = 0.05;
const rot_speed = orb_speed;

// Add light
const sunlight = new THREE.PointLight( 0xffffff, 1, 0, 1);
sunlight.position.set( 0, 0, 0);
scene.add(sunlight);

const ambient = new THREE.AmbientLight( 0x404040 );
scene.add( ambient );

// Declare orbital elements
const sun_geo = new THREE.SphereGeometry(8, 32, 32);
const sun_texture = new THREE.TextureLoader().load('./assets/2k_sun.jpg');
const sun_mat = new THREE.MeshBasicMaterial( { map: sun_texture } );

const sun = new THREE.Mesh( sun_geo, sun_mat );
scene.add( sun );

const earth_obj = new THREE.Object3D();

const earth_geo = new THREE.SphereGeometry(2, 16, 16);
const earth_texture = new THREE.TextureLoader().load('./assets/2k_earth_daymap.jpg');
const earth_mat = new THREE.MeshPhongMaterial( { map: earth_texture } );

const earth = new THREE.Mesh( earth_geo, earth_mat );
// earth.rotation.z = Math.PI;

const axis_geo = new THREE.CylinderGeometry(0.1, 0.1, 5);
const axis_mat = new THREE.MeshBasicMaterial( {color: 0x00ffff } );
const axis = new THREE.Mesh(axis_geo, axis_mat);

earth_obj.add(axis);
earth_obj.add( earth );
scene.add(earth_obj);

// Rotate Earth axis
// earth_obj.rotateZ(23.5 * Math.PI / 180.0);

// const star_geo = new THREE.SphereGeometry(500, 64, 64);
// const star_mat = new THREE.MeshBasicMaterial({
//     map: new THREE.TextureLoader().load('./assets/2k_stars.jpg'),
//     side: THREE.DoubleSide,
//     shininess: 0
// });
// const stars = new THREE.Mesh(star_geo, star_mat);


// Create orbit
const orbit_curve = new THREE.EllipseCurve(
	0,  0,            // ax, aY
	24, 24,           // xRadius, yRadius
	0,  2 * Math.PI,  // aStartAngle, aEndAngle
	false,            // aClockwise
	0                 // aRotation
);

// scene.add( stars );

// Move Camera to position
camera2.position.set(0, 0, 40);
camera2.lookAt(0, 0, 0);

// Orbital Parameters
let eccen = 0.3;
let omega = 0.0;
let focus = eccen * orbit_curve.xRadius;

function updateOrbit() {
    let points = orbit_curve.getPoints( 120 );
    let orbit_geo = new THREE.BufferGeometry().setFromPoints( points ).rotateX(Math.PI / 2);
    let orbit_mat = new THREE.LineBasicMaterial( { color: 0xffff00 } );
    
    let orbit = new THREE.Line( orbit_geo, orbit_mat );
    
    // Add objects to scene
    scene.add( orbit );
}

function updateEccentricity() {
    focus = eccen * orbit_curve.xRadius; 
    orbit_curve.yRadius = Math.sqrt( Math.pow(orbit_curve.xRadius, 2) - Math.pow(focus, 2));
    orbit_curve.aX = focus;
    updateOrbit();
}

function updatePrecession() {
    // omega += 180.0

    let axisXrotation = 23.5 * Math.sin (omega * Math.PI / 180.0);
    let axisZrotation = 23.5 * Math.cos (omega * Math.PI / 180.0);
    let rot = new THREE.Euler(axisXrotation * Math.PI / 180.0, 0, axisZrotation * Math.PI / 180.0, 'XYZ');

    earth_obj.setRotationFromEuler(rot);
    // earth_obj.rotateZ(23.5 * Math.PI / 180.0);
}

function setEarthRotation() {
    earth.rotation.y += rot_speed;
}

function setEarthPosition( dt ) {
    let at = (dt * orb_speed) % 1;
    let pos = orbit_curve.getPointAt( at );

    earth_obj.position.x = pos.x;
    earth_obj.position.z = -pos.y;
}

function animate() {
    requestAnimationFrame( animate );

    updateEccentricity();
    updatePrecession();

    //run_time += 1;
    run_time = clock.getElapsedTime();
    setEarthPosition( run_time ); 
    setEarthRotation( clock.getDelta() );

    renderer.render( scene, camera2 );
}

// Set up time and start animation
clock.start();
let run_time = clock.getElapsedTime();
animate();