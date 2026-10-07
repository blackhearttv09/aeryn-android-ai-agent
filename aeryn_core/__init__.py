package com.aeryn.agent

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class AerynBootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val serviceIntent = Intent(context, AerynForegroundService::class.java)
            context.startForegroundService(serviceIntent)
        }
    }
}

