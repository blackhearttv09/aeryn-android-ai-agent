package com.aeryn.agent

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class AerynActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val serviceIntent = Intent(this, AerynForegroundService::class.java)
        startForegroundService(serviceIntent)
    }
}
