package fr.utbm.vrp.agents;

import fr.utbm.vrp.agents.TaskAgent;
import io.sarl.core.Initialize;
import io.sarl.core.Lifecycle;
import io.sarl.core.Logging;
import io.sarl.lang.annotation.ImportedCapacityFeature;
import io.sarl.lang.annotation.PerceptGuardEvaluator;
import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Agent;
import io.sarl.lang.core.AtomicSkillReference;
import io.sarl.lang.core.DynamicSkillProvider;
import io.sarl.lang.core.Event;
import io.sarl.lang.scoping.extensions.cast.PrimitiveCastExtensions;
import java.io.StringReader;
import java.util.Collection;
import java.util.Iterator;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;
import javax.inject.Inject;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.xbase.lib.Extension;
import org.eclipse.xtext.xbase.lib.Pure;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 * Boot agent
 * <br>His goal is just to launch the task agent and then die
 * 
 * <br>MAS Systems based on <a href=https://www.semanticscholar.org/paper/Agents-towards-vehicle-routing-problems-Vokr%C3%ADnek-Komenda/1d486f85f0810331c8feb203ac126a7c192d00e1#related-papers>Agents towards vehicle routing problems</a> article
 * <br>Strategy implemented: FIFO-ITER-CNP-RA
 */
@SarlSpecification("0.12")
@SarlElementType(19)
@SuppressWarnings("all")
public class BootAgent extends Agent {
  private void $behaviorUnit$Initialize$0(final Initialize occurrence) {
    try {
      Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.setLoggingName("Boot agent");
      Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("The program has been launched.");
      Object _get = occurrence.parameters[0];
      String json_string = (_get == null ? null : _get.toString());
      json_string = json_string.replace("\'", "\"");
      Object json_objc = null;
      JSONParser _jSONParser = new JSONParser();
      StringReader _stringReader = new StringReader(json_string);
      json_objc = _jSONParser.parse(_stringReader);
      JSONObject json_builded = ((JSONObject) json_objc);
      ConcurrentLinkedQueue<String> customers_list = new ConcurrentLinkedQueue<String>();
      Object _get_1 = json_builded.get("customers");
      JSONArray jsonArray = ((JSONArray) _get_1);
      Iterator<Object> iterator = jsonArray.iterator();
      while (iterator.hasNext()) {
        Object _next = iterator.next();
        customers_list.add((_next == null ? null : _next.toString()));
      }
      Object _get_2 = json_builded.get("depot");
      String depot = (_get_2 == null ? null : _get_2.toString());
      Object _get_3 = json_builded.get("vehicle_capacity");
      int vehicle_capacity_raw = ((_get_3 == null ? null : _get_3.toString()) == null ? 0 : PrimitiveCastExtensions.intValue((_get_3 == null ? null : _get_3.toString())));
      AtomicInteger vehicle_capacity = new AtomicInteger(vehicle_capacity_raw);
      Object _get_4 = json_builded.get("topic");
      String topic = (_get_4 == null ? null : _get_4.toString());
      Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.spawn(TaskAgent.class, depot, customers_list, vehicle_capacity, topic);
      Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER_1.killMe();
    } catch (Throwable _e) {
      throw Exceptions.sneakyThrow(_e);
    }
  }
  
  @Extension
  @ImportedCapacityFeature(Lifecycle.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_LIFECYCLE;
  
  @SyntheticMember
  @Pure
  private Lifecycle $CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE == null || this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE = $getSkill(Lifecycle.class);
    }
    return $castSkill(Lifecycle.class, this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE);
  }
  
  @Extension
  @ImportedCapacityFeature(Logging.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_LOGGING;
  
  @SyntheticMember
  @Pure
  private Logging $CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_LOGGING == null || this.$CAPACITY_USE$IO_SARL_CORE_LOGGING.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_LOGGING = $getSkill(Logging.class);
    }
    return $castSkill(Logging.class, this.$CAPACITY_USE$IO_SARL_CORE_LOGGING);
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$Initialize(final Initialize occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$Initialize$0(occurrence));
  }
  
  @SyntheticMember
  @Override
  public void $getSupportedEvents(final Set<Class<? extends Event>> toBeFilled) {
    super.$getSupportedEvents(toBeFilled);
    toBeFilled.add(Initialize.class);
  }
  
  @SyntheticMember
  @Override
  public boolean $isSupportedEvent(final Class<? extends Event> event) {
    if (Initialize.class.isAssignableFrom(event)) {
      return true;
    }
    return false;
  }
  
  @SyntheticMember
  @Override
  public void $evaluateBehaviorGuards(final Object event, final Collection<Runnable> callbacks) {
    super.$evaluateBehaviorGuards(event, callbacks);
    if (event instanceof Initialize) {
      final Initialize occurrence = (Initialize) event;
      $guardEvaluator$Initialize(occurrence, callbacks);
    }
  }
  
  @SyntheticMember
  public BootAgent(final UUID parentID, final UUID agentID) {
    super(parentID, agentID);
  }
  
  @SyntheticMember
  @Inject
  public BootAgent(final UUID parentID, final UUID agentID, final DynamicSkillProvider skillProvider) {
    super(parentID, agentID, skillProvider);
  }
}
