package com.example.leitorgabarito

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import android.provider.MediaStore
import android.support.v4.app.ActivityCompat
import android.support.v4.content.ContextCompat
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*

class MainActivity : AppCompatActivity() {

    private val REQUEST_CODE = 1
    val TagDebug = "LeitorGabarito"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        setupPermissions()

        fab.setOnClickListener { view ->
            checkCameraHardware(this)
        }
    }

    private fun setupPermissions() {
        val permission = ContextCompat.checkSelfPermission(this,
            Manifest.permission.CAMERA)

        ActivityCompat.requestPermissions(this,
            arrayOf(Manifest.permission.CAMERA),
            0);

        if (permission != PackageManager.PERMISSION_GRANTED) {
            Log.i(TagDebug, "Permission to record denied")
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }

    fun openCamera(){


        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        startActivityForResult(intent, REQUEST_CODE)
    }

    private fun checkCameraHardware(context: Context) {
        if (context.packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            openCamera()
        } else {
            Toast.makeText(this,"Este dispositivo não possui câmera",Toast.LENGTH_LONG)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
//        super.onActivityResult(requestCode, resultCode, data)

        if(requestCode == this.REQUEST_CODE && resultCode == RESULT_OK){
            try {
                imageView.setImageBitmap(data!!.extras.get("data") as Bitmap)
            }catch (e:Exception){
                Log.e(TagDebug,e.message)
            }
        }
    }



}
