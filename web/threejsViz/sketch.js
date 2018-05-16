/*  Based on
 *  Word Land  -  A 3D visualization for movie script and word2vec
 *  Yuli Cai
 *  2018
 */


var text_title = location.href.split("/").slice(-1) + "";
text_title = text_title.replace(".html",""); 

const path_to_file = "data/"+ text_title +"/emoVec_3d_50.json";
const mappingVec_path = "data/drinkVec_3d_50.json";
const path_3 = "data/"+ text_title +"/joinEmoVec_3d_50.json";

const emo_list = "data/emoList.txt"
var is_searching_words = false;
const first_word = "love";
const second_word = "human";


var camera, scene, scenelight, renderer, controls;
var cameraSpeed = 0;

const mapping_range = 40.;

////////////////////////////////
//----- Pointer Lock --------//
////////////////////////////////

var blocker = document.getElementById('blocker');
var instructions = document.getElementById('instructions');

// http://www.html5rocks.com/en/tutorials/pointerlock/intro/
var havePointerLock = 'pointerLockElement' in document || 'mozPointerLockElement' in document || 'webkitPointerLockElement' in document;
if (havePointerLock) {
    var element = document.body;
    var pointerlockchange = function(event) {
        if (document.pointerLockElement === element || document.mozPointerLockElement === element || document.webkitPointerLockElement === element) {
            controlsEnabled = true;
            controls.enabled = true;
            blocker.style.display = 'none';
        } else {
            controls.enabled = false;
            blocker.style.display = 'block';
            instructions.style.display = '';
        }
    };


    var pointerlockerror = function(event) {
        instructions.style.display = '';
    };

    // Hook pointer lock state change events
    document.addEventListener('pointerlockchange', pointerlockchange, false);
    document.addEventListener('mozpointerlockchange', pointerlockchange, false);
    document.addEventListener('webkitpointerlockchange', pointerlockchange, false);
    document.addEventListener('pointerlockerror', pointerlockerror, false);
    document.addEventListener('mozpointerlockerror', pointerlockerror, false);
    document.addEventListener('webkitpointerlockerror', pointerlockerror, false);
    instructions.addEventListener('click', function(event) {
        instructions.style.display = 'none';
        // Ask the browser to lock the pointer
        element.requestPointerLock = element.requestPointerLock || element.mozRequestPointerLock || element.webkitRequestPointerLock;
        element.requestPointerLock();
    }, false);
} else {
    instructions.innerHTML = 'Your browser doesn\'t seem to support Pointer Lock API';
}
var controlsEnabled = false;
var moveForward = false;
var moveBackward = false;
var moveLeft = false;
var moveRight = false;
var moveUp = false;
var moveDown = false;
var onAmerica = false;
var onPeace = false;


////////////////////////////////
//----- Control Speed --------//
////////////////////////////////

var prevTime = performance.now();
var velocity = new THREE.Vector3();
var direction = new THREE.Vector3();
const time2find = 100;
var counter = 100;



////////////////////////////////
//----- Text Data --------//
////////////////////////////////

var data, data2, data3;
var emoList;
var words_array;
var word1, word2;
var word1Pos = { x: 0, y: 0, z: 0 };
var word2Pos = { x: 0, y: 0, z: 0 };
var speed2word1, speed2word2;

preload(loadThirdList);



////////////////////////////////
//----- Preload --------//
////////////////////////////////

function loadSecondList(callback) {
    var xobj = new XMLHttpRequest();
    xobj.open('GET', mappingVec_path);
    xobj.responseType = "json";
    xobj.send();
    xobj.onload = function() {
        data2 = xobj.response;
        callback();
    }
}

function loadThirdList(callback) {
    var xobj = new XMLHttpRequest();
    xobj.open('GET', path_3);
    xobj.responseType = "json";
    xobj.send();
    xobj.onload = function() {
        data3 = xobj.response;
        callback();
    }
}

// Load JSON data file
function preload() {
    var xobj = new XMLHttpRequest();
    xobj.open('GET', path_to_file);
    xobj.responseType = "json";
    xobj.send();
    xobj.onload = function() {
        data = xobj.response;
        loadSecondList(function(){
            loadThirdList(init)
        });
    }
}

function filter(words_array) {
    var list = [];
    for (i in words_array) {
        var word = words_array[i];
        if (emoList.indexOf(word) > -1) list.push(word);
    }
    console.log("Filter result:")
    console.log(list);
    return list;
}

function generateMesh(data, style, font, mapping_range) {
    console.log(data)
    words_array = Object.keys(data);
    for (var i = 0; i < words_array.length; i++) {
            var message = words_array[i];
            var x = (data[message][0]);
            var y = (data[message][1]);
            var z = (data[message][2]);
            var mappedX = Math.floor(mapping(x, -17., 18., -mapping_range / 2., mapping_range));
            var mappedY = Math.floor(mapping(y, -17., 18., -mapping_range / 2., mapping_range));
            var mappedZ = Math.floor(mapping(z, -17., 18., -mapping_range / 2., mapping_range));
            // Main function to generate three.js mesh from a word
            if (message == word1 || message == word2) generateShapeFromText(message, mappedX, mappedY, mappedZ, font, specialMat);
            else generateShapeFromText(message, mappedX, mappedY, mappedZ, font, style);
        }
}

////////////////////////////////
//----- INIT --------//
////////////////////////////////


function init() {

    var textColor = 0xffffff;
    var textColor2 = 0xff4c4c;
    var textColor3 = 0xaaffaa;
    var bgColor = 0x000000;
    var lightColor = 0xffffff;


    // Save all the words in an array

    if (is_searching_words) {
        // Get the data from two high light words
        word1 = first_word;
        word2 = second_word;
        word1Pos.x = data[word1][0];
        word1Pos.y = data[word1][1];
        word1Pos.z = data[word1][2];
        word1Pos.x = Math.floor(mapping(word1Pos.x, -17., 18., -mapping_range / 2, mapping_range));
        word1Pos.y = Math.floor(mapping(word1Pos.y, -17., 18., -mapping_range / 2, mapping_range));
        word1Pos.z = Math.floor(mapping(word1Pos.z, -17., 18., -mapping_range / 2., mapping_range));


        word2Pos.x = data[word2][0];
        word2Pos.y = data[word2][1];
        word2Pos.z = data[word2][2];
        word2Pos.x = Math.floor(mapping(word2Pos.x, -17., 18., -mapping_range / 2., mapping_range));
        word2Pos.y = Math.floor(mapping(word2Pos.y, -17., 18., -mapping_range / 2., mapping_range));
        word2Pos.z = Math.floor(mapping(word2Pos.z, -17., 18., -mapping_range / 2., mapping_range));
        // Calculate the distance between this two words
        var _diff = (diff(word1Pos.x, word1Pos.y, word1Pos.z, word2Pos.x, word2Pos.y, word2Pos.z)).toFixed(2);
        document.getElementById("text_info").innerHTML = "In the text " + text_title + " <br /> <span style=\"color:#ff5935; font-size:14x\">" + word1 + " </span> and <span style=\"color:#ff5935; font-size:17px\"> " + word2 + " </span> <br /> are <span style=\"color:#ff5935\">" + _diff + " </span> pixels <br /> away from each other.";
    } else {
        console.log("test");
        document.getElementById("text_info").innerHTML = "Current Vector Space:  " + text_title;

    }

    // Initials for THREE.JS

    //Set up Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, -0, 400);

    // Set up a new scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(bgColor);
    scene.fog = new THREE.Fog(bgColor, 0, 850);

    // Control system
    controls = new THREE.PointerLockControls(camera);
    scene.add(controls.getObject());

    // Lighting
    // scenelight = new THREE.AmbientLight(0x404040);
    scenelight = new THREE.AmbientLight(lightColor);
    scene.add(scenelight);

    // Load word with font
    var loader = new THREE.FontLoader();
    loader.load('fonts/helvetiker_regular.typeface.json', function(font) {

        // Material for normal text
        var matLite = new THREE.MeshPhongMaterial({
            color: textColor,
            shininess: 35,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide
        });
        var matLite2 = new THREE.MeshPhongMaterial({
            color: textColor2,
            shininess: 35,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide
        });
        var matLite3 = new THREE.MeshPhongMaterial({
            color: textColor3,
            shininess: 35,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide
        });
        // Material for high-light text
        var specialMat = new THREE.MeshPhongMaterial({
            color: 0xf45342,
            side: THREE.DoubleSide,
            shininess: 35,
            transparent: true,
            opacity: 0.8
        });
        // Go through the data array and create a three.js mesh from each word
        generateMesh(data, matLite, font,mapping_range)
        generateMesh(data2, matLite2, font, mapping_range)
        generateMesh(data3, matLite3, font, mapping_range/1.5)
    }); //end load function

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    window.addEventListener('resize', onWindowResize, false);

    animate();
} // end init



////////////////////////////////
//- Generate Mesh from word --//
////////////////////////////////

function generateShapeFromText(_word, _xpos, _ypos, _zpos, _font, mL) {
    var xMid, text;
    var textShape = new THREE.BufferGeometry();

    var shapes = _font.generateShapes(_word, 10, 1); //text,size,divisions
    // Create a new geometry from the font shape
    var geometry = new THREE.ShapeGeometry(shapes);
    geometry.computeBoundingBox();
    // xMid = _pos - 0.5 * (geometry.boundingBox.max.x - geometry.boundingBox.min.x);
    // geometry.translate(xMid, 0, 0);
    geometry.translate(_xpos, _ypos, 0);

    // make shape ( N.B. edge view not visible )
    textShape.fromGeometry(geometry);
    // Apply material with geometry
    text = new THREE.Mesh(textShape, mL);
    text.position.z = _zpos;
    scene.add(text);

}


////////////////////////////////
//----- Animate --------------//
////////////////////////////////

function animate() {
    requestAnimationFrame(animate);
    render();
}



////////////////////////////////
//----- Render --------------//
////////////////////////////////

function render() {
    if (controlsEnabled === true) {
        var time = performance.now();
        var delta = (time - prevTime) / 1000;
        velocity.x -= velocity.x * 5.0 * delta;
        velocity.z -= velocity.z * 1.0 * delta;
        velocity.y -= velocity.y * 5.0 * delta;
        // velocity.y -= 9.8 * 100.0 * delta; // 100.0 = mass

        //Direction is polarized, either 1 or -1
        direction.z = Number(moveForward) - Number(moveBackward);
        direction.x = Number(moveLeft) - Number(moveRight);
        direction.y = Number(moveDown) - Number(moveUp);
        direction.normalize(); // this ensures consistent movements in all directions
        if (moveForward || moveBackward) velocity.z -= direction.z * 400.0 * delta;
        if (moveLeft || moveRight) velocity.x -= direction.x * 400.0 * delta;
        if (moveUp || moveDown) velocity.y -= direction.y * 400 * delta;

        // More the control perspective
        controls.getObject().translateX(velocity.x * delta);
        controls.getObject().translateY(velocity.y * delta);
        controls.getObject().translateZ(velocity.z * delta);

        // Go find word1
        if (onAmerica) {
            if (counter > 0) {
                controls.getObject().translateX(speed2word1.x);
                controls.getObject().translateY(speed2word1.y);
            } else {
                counter = time2find;
                onAmerica = false;
            }
            counter--;
        }
        // Go find word2
        if (onPeace) {
            if (counter > 0) {
                controls.getObject().translateX(speed2word2.x);
                controls.getObject().translateY(speed2word2.y);
            } else {
                counter = time2find;
                onPeace = false;
            }
            counter--;
        }
        prevTime = time;
    }

    renderer.render(scene, camera);
}


function onKeyDown(event) {
    switch (event.keyCode) {
        case 38: // up
            moveUp = true;
            break;
        case 87: // w
            moveForward = true;
            break;
        case 37: // left
            onAmerica = false;
            break;
        case 65: // a
            moveLeft = true;
            break;
        case 40: // down
            moveDown = true;
            break;
        case 83: // s
            moveBackward = true;
            break;
        case 39: // right
            onPeace = false;
            break;
        case 68: // d
            moveRight = true;
            break;
    }
}


function onKeyUp(event) {
    switch (event.keyCode) {
        case 38: // up
            moveUp = false;
            break;
        case 40: // down
            moveDown = false;
            break;
        case 87: // w
            moveForward = false;
            break;
        case 65: // a
            moveLeft = false;
            break;

        case 83: // s
            moveBackward = false;
            break;

        case 68: // d
            moveRight = false;
            break;
        case 37: // left
            // Press left key move to the first word
            onAmerica = true;
            var currentX = controls.getObject().position.x;
            var currentY = controls.getObject().position.y;
            var diff_word1_x = word1Pos.x - currentX;
            var diff_word1_y = word1Pos.y - currentY;

            if (Math.abs(diff_word1_y) < 5 && Math.abs(diff_word1_x) < 5) speed2word1 = { x: 0, y: 0 };
            else speed2word1 = { x: diff_word1_x / counter, y: diff_word1_y / counter };
            break;
        case 39: // right
            // Press right key move to the second word
            onPeace = true;
            var currentX = controls.getObject().position.x;
            var currentY = controls.getObject().position.y;
            var diff_word2_x = word2Pos.x - currentX;
            var diff_word2_y = word2Pos.y - currentY;
            if (Math.abs(diff_word2_y) < 5 && Math.abs(diff_word2_x) < 5) speed2word2 = { x: 0, y: 0 };
            else speed2word2 = { x: diff_word2_x / counter, y: diff_word2_y / counter };
            break;
    }
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}


function mapping(n, start1, stop1, start2, stop2) {
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2;
}

function diff(x1, y1, z1, x2, y2, z2) {
    return Math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2));
}


document.addEventListener('keydown', onKeyDown, false);
document.addEventListener('keyup', onKeyUp, false);