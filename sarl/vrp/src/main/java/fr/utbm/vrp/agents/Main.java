package fr.utbm.vrp.agents;

import io.sarl.bootstrap.SRE;
import io.sarl.bootstrap.SREBootstrap;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;



/** 
 * Main
 * <br>Main that subscribes to a JEDIS post and launch multiagent system when topic is active 
 */
public class Main {
	
    private static final String JEDIS_HOST = "127.0.0.1";
    private static final int JEDIS_PORT = 6379;

    public static void main(String[] args) throws InterruptedException {
        new Main().run();
    }

    private void run() throws InterruptedException {
        JedisPubSub jedisPubSub = setupSubscriber();
    }

    private JedisPubSub setupSubscriber() {
        final JedisPubSub jedisPubSub = new JedisPubSub() {
            @Override
        	public void onMessage (String channel, String message) {
        		System.out.println("Channel: " + channel + " Message: " + message);
        	    SREBootstrap bootstrap = SRE.getBootstrap();
        	    try {
					bootstrap.startAgent(BootAgent.class);
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
        	}
//            public void onMessage(String channel, String message) {
//                System.out.println(message);
//            }
        };
        new Thread(() -> {
            Jedis jedis = new Jedis(JEDIS_HOST, JEDIS_PORT);
            jedis.subscribe(jedisPubSub, "sarlTopic");
            while(true){
            }
        }, "subscriberThread").start();
        return jedisPubSub;
    }
    /**
	 * Callback after receiving the message
	 */


}